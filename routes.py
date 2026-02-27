from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config_db import get_db_connection
import bcrypt
import uuid
routes = Blueprint('routes', __name__)

# =====================================================
# HOME ROUTE
# =====================================================

@routes.route('/', methods=['GET'])
def home():
    """

    ---
    tags:
      - Home
    responses:
      200:
        description: Welcome message
    """
    return jsonify({"message": "Welcome to the Task Management API 🚀"}), 200



# =====================================================
# REGISTER ROUTE
# =====================================================
@routes.route('/register', methods=['POST'])
def register():
    """
    Register New User
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
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
              example: 123456
    responses:
      201:
        description: User registered successfully
      400:
        description: Bad request
      409:
        description: Username already exists
      500:
        description: Server error
    """

    data = request.get_json()

    if not data:
        return jsonify({"msg": "Request body required"}), 400

    username = data.get("cms_username")
    password = data.get("cms_password")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    conn, cursor = get_db_connection()

    try:
        cursor.execute(
            "SELECT 1 FROM tbl_login WHERE cms_username = %s",
            (username,)
        )
        if cursor.fetchone():
            return jsonify({"msg": "Username already exists"}), 409

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute("""
            INSERT INTO tbl_login (
                cmi_emp_id,
                cms_username,
                cms_password,
                cmi_role,
                cmb_dashboard,
                cmb_manage_emp,
                cmb_create_task,
                cmb_all_task,
                cmb_requests,
                cmb_emp_requests,
                cmb_create_micro_tasks
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            1,
            username,
            hashed_password,
            1,
            True,
            True,
            True,
            True,
            True,
            True,
            True
        ))

        conn.commit()
        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        conn.rollback()
        print("REGISTER ERROR:", e)
        return jsonify({"msg": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# =====================================================
# LOGIN ROUTE
# =====================================================

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
              example: deepali123
            cms_password:
              type: string
              example: MyPassword@123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      400:
        description: Bad request
      500:
        description: Internal server error
    """

    data = request.get_json()

    if not data:
        return jsonify({"msg": "Request body required"}), 400

    username = data.get("cms_username")
    password = data.get("cms_password")

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    conn, cursor = get_db_connection()

    try:
        cursor.execute(
            "SELECT cms_password FROM tbl_login WHERE cms_username = %s",
            (username,)
        )

        result = cursor.fetchone()

        if not result:
            return jsonify({"msg": "Invalid credentials"}), 401

        stored_password = result[0]

        if not stored_password:
            return jsonify({"msg": "Invalid credentials"}), 401

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):
            access_token = create_access_token(identity=username)
            return jsonify({
                "msg": "Login successful",
                "access_token": access_token
            }), 200

        return jsonify({"msg": "Invalid credentials"}), 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"msg": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
# =====================================================
# GET MY TASKS
# =====================================================

@routes.route('/my-tasks', methods=['GET'])
@jwt_required()
def get_user_tasks():
    """
    Get My Tasks
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: List of tasks
      401:
        description: Unauthorized
    """

    current_user = get_jwt_identity()

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    try:
        cursor.execute(
            "SELECT cmi_emp_id FROM tbl_login WHERE cms_username = %s",
            (current_user,)
        )

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

        task_list = [
            {
                "task_id": t[0],
                "task_desc": t[1],
                "task_title": t[2]
            }
            for t in tasks
        ]

        return jsonify({"tasks": task_list}), 200

    except Exception as e:
        print("TASK ERROR:", e)
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()


# =====================================================
# CREATE TASK
# =====================================================

@routes.route('/create-task', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    data = request.get_json()

    task_title = data.get("task_title")
    task_desc = data.get("task_desc")
    allocated_to = data.get("allocated_to")
    task_deadline = data.get("task_deadline")

    if not (task_title and task_desc and allocated_to and task_deadline):
        return jsonify({"msg": "All fields are required"}), 400

    conn, cursor = get_db_connection()

    try:
        cursor.execute("""
            INSERT INTO tbl_task
            (cms_task_title, cms_task_desc, cmi_allocated_to, cmd_task_deadline)
            VALUES (%s, %s, %s, %s)
            RETURNING cmi_task_id
        """, (task_title, task_desc, allocated_to, task_deadline))

        task_id = cursor.fetchone()[0]
        conn.commit()

        return jsonify({"msg": "Task created successfully", "task_id": task_id}), 201

    except Exception as e:
        print("CREATE ERROR:", e)
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()


# =====================================================
# UPDATE TASK
# =====================================================

@routes.route('/update-task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    data = request.get_json()
    task_title = data.get("task_title")
    task_desc = data.get("task_desc")
    allocated_to = data.get("allocated_to")

    conn, cursor = get_db_connection()

    try:
        cursor.execute(
            "SELECT 1 FROM tbl_task WHERE cmi_task_id = %s",
            (task_id,)
        )

        if not cursor.fetchone():
            return jsonify({"msg": "Task not found"}), 404

        cursor.execute("""
            UPDATE tbl_task
            SET cms_task_title = %s,
                cms_task_desc = %s,
                cmi_allocated_to = %s
            WHERE cmi_task_id = %s
        """, (task_title, task_desc, allocated_to, task_id))

        conn.commit()
        return jsonify({"msg": "Task updated successfully"}), 200

    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()


# =====================================================
# DELETE TASK
# =====================================================

@routes.route('/delete-task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    conn, cursor = get_db_connection()

    try:
        cursor.execute(
            "SELECT 1 FROM tbl_task WHERE cmi_task_id = %s",
            (task_id,)
        )

        if not cursor.fetchone():
            return jsonify({"msg": "Task not found"}), 404

        cursor.execute(
            "DELETE FROM tbl_task WHERE cmi_task_id = %s",
            (task_id,)
        )

        conn.commit()
        return jsonify({"msg": "Task deleted successfully"}), 200

    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"msg": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()
