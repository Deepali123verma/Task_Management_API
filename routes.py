from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config_db import get_db_connection

routes = Blueprint('routes', __name__)

# LOGIN ROUTE
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection error"}), 500

    cursor.execute("SELECT cmi_emp_id, cms_password FROM tbl_login WHERE cms_username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and password == user[1]:
        access_token = create_access_token(identity=str(user[0]))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401


#  (Protected Route)
@routes.route('/tasks/assigned', methods=['POST'])
@jwt_required()
def get_assigned_tasks():
    emp_id = int(get_jwt_identity())  # Fetch from token

    conn, cursor = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection error"}), 500

    cursor.execute(
        "SELECT cms_task_title, cms_task_desc FROM tbl_task WHERE cmi_allocated_to = %s",
        (emp_id,)
    )
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    if tasks:
        task_list = [{"title": t[0], "description": t[1]} for t in tasks]
        return jsonify({"emp_id": emp_id, "assigned_tasks": task_list}), 200
    else:
        return jsonify({"msg": f"No tasks found for employee ID: {emp_id}"}), 404

