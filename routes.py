from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config_db import get_db_connection

routes = Blueprint('routes', __name__)

# LOGIN ROUTE
@routes.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - cms_username
            - cms_password
          properties:
            cms_username:
              type: string
              example: deepali
            cms_password:
              type: string
              example: mypassword
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
      400:
        description: Missing username or password
      401:
        description: Invalid credentials
      500:
        description: Database error
    """
    data = request.get_json()

    username = data.get('cms_username')
    password = data.get('cms_password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        query = """
            SELECT * FROM tbl_login WHERE cms_username = %s AND cms_password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# MY TASKS ROUTE
@routes.route('/my-tasks', methods=['POST'])
@jwt_required()
def get_user_tasks_post():
    """
    Get tasks assigned to the logged-in user
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: List of tasks assigned to the user
        schema:
          type: object
          properties:
            tasks:
              type: array
              items:
                type: object
                properties:
                  task_id:
                    type: integer
                    example: 1
                  task_desc:
                    type: string
                    example: "Complete backend API integration"
                  task_title:
                    type: string
                    example: "Backend API"
      401:
        description: Unauthorized - missing or invalid token
      404:
        description: No tasks found for user
      500:
        description: Database error
    """
    current_user = get_jwt_identity()  # cms_username

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        # Step 1: Get emp_id of current user from tbl_login
        cursor.execute("SELECT cmi_emp_id FROM tbl_login WHERE cms_username = %s", (current_user,))
        emp_result = cursor.fetchone()

        if not emp_result:
            return jsonify({"msg": "User not found"}), 404

        emp_id = emp_result[0]  # cmi_emp_id

        # Step 2: Fetch tasks assigned to this emp_id
        cursor.execute("""
            SELECT cmi_task_id, cms_task_desc, cms_task_title
            FROM tbl_task
            WHERE cmi_allocated_to = %s
        """, (emp_id,))
        tasks = cursor.fetchall()

        if not tasks:
            return jsonify({"msg": "No tasks found for user"}), 404

        task_list = []
        for task in tasks:
            task_list.append({
                "task_id": task[0],
                "task_desc": task[1],
                "task_title": task[2]
            })

        return jsonify({"tasks": task_list}), 200

    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

