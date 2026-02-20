from datetime import datetime
import uuid
from config_db import db


# =====================================
# Employee Model
# =====================================
class Employee(db.Model):
    __tablename__ = "tbl_employee"

    cmu_guid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cmi_emp_id = db.Column(db.Integer, unique=True, nullable=False)

    cms_emp_first_name = db.Column(db.String, nullable=False)
    cms_emp_middle_name = db.Column(db.String)
    cms_emp_last_name = db.Column(db.String)

    cmi_phone_number = db.Column(db.String)
    cms_email_id = db.Column(db.String, unique=True)
    cms_documents_link = db.Column(db.Text)

    # Relationships
    login = db.relationship("Login", backref="employee", uselist=False)
    tasks_created = db.relationship("TLTask", foreign_keys="TLTask.cmi_assigned_by", backref="creator")
    tasks_assigned = db.relationship("TLTask", foreign_keys="TLTask.cmi_assigned_to", backref="assignee")


# =====================================
# Login Model
# =====================================
class Login(db.Model):
    __tablename__ = "tbl_login"

    cmu_guid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cmi_emp_id = db.Column(db.Integer, db.ForeignKey("tbl_employee.cmi_emp_id"), nullable=False)

    cms_username = db.Column(db.String, unique=True, nullable=False)
    cms_password = db.Column(db.Text, nullable=False)

    cmi_role = db.Column(db.Integer)

    cmb_dashboard = db.Column(db.Boolean, default=False)
    cmb_manage_emp = db.Column(db.Boolean, default=False)
    cmb_create_task = db.Column(db.Boolean, default=False)
    cmb_all_task = db.Column(db.Boolean, default=False)
    cmb_requests = db.Column(db.Boolean, default=False)
    cmb_emp_requests = db.Column(db.Boolean, default=False)
    cmb_create_micro_tasks = db.Column(db.Boolean, default=False)


# =====================================
# TL Task Model
# =====================================
class TLTask(db.Model):
    __tablename__ = "tbl_tl_task"

    cms_guid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cmi_task_id = db.Column(db.Integer, nullable=False)

    cms_task_title = db.Column(db.String, nullable=False)
    cms_task_desp = db.Column(db.Text)
    cmt_deadline = db.Column(db.DateTime)

    cmi_assigned_by = db.Column(db.Integer, db.ForeignKey("tbl_employee.cmi_emp_id"))
    cmi_assigned_to = db.Column(db.Integer, db.ForeignKey("tbl_employee.cmi_emp_id"))

    progress_updates = db.relationship(
        "TaskProgress",
        backref="task",
        cascade="all, delete-orphan"
    )


# =====================================
# Task Progress Model
# =====================================
class TaskProgress(db.Model):
    __tablename__ = "tbl_task_progress"

    cms_guid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    cmi_task_id = db.Column(db.Integer, db.ForeignKey("tbl_tl_task.cmi_task_id"), nullable=False)
    cmi_assigned_to = db.Column(db.Integer)

    cms_resolve_pass = db.Column(db.String)
    cms_remark = db.Column(db.Text)
    cms_pdf = db.Column(db.Text)

    cmd_timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# =====================================
# Employee Designation
# =====================================
class EmployeeDesignation(db.Model):
    __tablename__ = "tbl_employee_designation"

    id = db.Column(db.Integer, primary_key=True)

    cmi_emp_id = db.Column(db.Integer, db.ForeignKey("tbl_employee.cmi_emp_id"), nullable=False)
    cmi_emp_department = db.Column(db.Integer)
    cmi_emp_designation = db.Column(db.Integer)
    cmi_employement_type = db.Column(db.Integer)

    cmd_date_from = db.Column(db.Date)
    cmd_date_to = db.Column(db.Date)


# =====================================
# Employee Pending
# =====================================
class EmployeePending(db.Model):
    __tablename__ = "tbl_employee_pending"

    cmu_guid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    cmi_request_id = db.Column(db.Integer, nullable=False)
    cmi_action_type = db.Column(db.Integer)

    cmj_emp_data = db.Column(db.JSON)
    cmi_performed_by = db.Column(db.Integer)

    cms_status = db.Column(db.String)
    cmd_approved_at = db.Column(db.DateTime)
    cmi_approved_by = db.Column(db.Integer)
    cms_remark = db.Column(db.Text)


# =====================================
# Master Table
# =====================================
class Master(db.Model):
    __tablename__ = "tbl_master_2"

    cms_uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    cmi_master_code = db.Column(db.Integer, nullable=False)
    cms_master_code_description = db.Column(db.String)
    cmi_parent_code = db.Column(db.Integer)