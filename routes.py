from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config_db import get_db_connection
import bcrypt

routes = Blueprint('routes', __name__)

# HOME ROUTE
@routes.route('/')
def home():
    """
    Welcome Route
    ---
    tags:
      - Home
    responses:
      200:
        description: Welcome message for Task Management API
    """
    return jsonify({"message": "Welcome to the Task Management API 🚀"}), 200


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
              example: admin
            cms_password:
              type: string
              example: Admin123
    responses:
      200:
        description: Successful login
      400:
        description: Username and password required
      401:
        description: Invalid credentials
      500:
        description: Server error
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
        # ✅ Fetch only the password column for the given username
        query = "SELECT cms_password FROM tbl_login WHERE cms_username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"msg": "Invalid credentials"}), 401

        stored_password = result[0]

        # Handle string vs bytea (PostgreSQL may store as BYTEA)
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        # Check password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            access_token = create_access_token(identity=username)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"msg": f"Server error: {str(e)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# MY TASKS ROUTE
@routes.route('/my-tasks', methods=['GET'])
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
        cursor.execute("SELECT cmi_emp_id FROM tbl_login WHERE cms_username = %s", (current_user,))
        emp_result = cursor.fetchone()

        if not emp_result:
            return jsonify({"msg": "User not found"}), 404

        emp_id = emp_result[0]

        cursor.execute("""
            SELECT cmi_task_id, cms_task_desc, cms_task_title
            FROM tbl_task
            WHERE cmi_allocated_to = %s
        """, (emp_id,))
        tasks = cursor.fetchall()

        if not tasks:
            return jsonify({"msg": "No tasks found for user"}), 404

        task_list = [{"task_id": t[0], "task_desc": t[1], "task_title": t[2]} for t in tasks]
        return jsonify({"tasks": task_list}), 200

    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# CREATE TASK ROUTE
@routes.route('/create-task', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    consumes:
      - application/json
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - task_title
            - task_desc
            - allocated_to
            - task_deadline
          properties:
            task_title:
              type: string
              example: "Backend API"
            task_desc:
              type: string
              example: "Complete backend API integration"
            allocated_to:
              type: integer
              example: 101
            task_deadline:
              type: string
              example: "2025-09-15 18:00:00"
    responses:
      201:
        description: Task created successfully
      400:
        description: Missing fields
      500:
        description: Database error
    """
    data = request.get_json()
    task_title = data.get("task_title")
    task_desc = data.get("task_desc")
    allocated_to = data.get("allocated_to")
    task_deadline = data.get("task_deadline")  # new line

    if not (task_title and task_desc and allocated_to and task_deadline):
        return jsonify({"msg": "All fields are required"}), 400

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        cursor.execute("""
            INSERT INTO tbl_task (cms_task_title, cms_task_desc, cmi_allocated_to, cmd_task_deadline)
            VALUES (%s, %s, %s, %s) RETURNING cmi_task_id
        """, (task_title, task_desc, allocated_to, task_deadline))
        task_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"msg": "Task created successfully", "task_id": task_id}), 201
    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# UPDATE TASK ROUTE
@routes.route('/update-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update an existing task
    ---
    tags:
      - Tasks
    consumes:
      - application/json
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            task_title:
              type: string
            task_desc:
              type: string
            allocated_to:
              type: integer
    responses:
      200:
        description: Task updated successfully
      404:
        description: Task not found
      500:
        description: Database error
    """
    data = request.get_json()
    task_title = data.get("task_title")
    task_desc = data.get("task_desc")
    allocated_to = data.get("allocated_to")

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        cursor.execute("SELECT cmi_task_id FROM tbl_task WHERE cmi_task_id = %s", (task_id,))
        if not cursor.fetchone():
            return jsonify({"msg": "Task not found"}), 404

        cursor.execute("""
            UPDATE tbl_task
            SET cms_task_title = %s, cms_task_desc = %s, cmi_allocated_to = %s
            WHERE cmi_task_id = %s
        """, (task_title, task_desc, allocated_to, task_id))
        conn.commit()
        return jsonify({"msg": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# DELETE TASK ROUTE
@routes.route('/delete-task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        required: true
        type: integer
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
      500:
        description: Database error
    """
    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        cursor.execute("SELECT cmi_task_id FROM tbl_task WHERE cmi_task_id = %s", (task_id,))
        if not cursor.fetchone():
            return jsonify({"msg": "Task not found"}), 404

        cursor.execute("DELETE FROM tbl_task WHERE cmi_task_id = %s", (task_id,))
        conn.commit()
        return jsonify({"msg": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": f"Database error: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
