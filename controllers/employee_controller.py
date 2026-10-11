# controllers/employee_controller.py
from flask import Blueprint, jsonify, request, render_template, redirect
from models.employee_model import employees

print (__name__)

employee_bp = Blueprint("employee_bp", __name__)

# READ ALL  ->  GET /employees
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(employees), 200

# READ ONE  ->  GET /employees/3
@employee_bp.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    for e in employees:
        if e["id"] == id:
            return jsonify(e), 200
    return jsonify({"error": "Not found"}), 404


@employee_bp.route("/employees/new", methods=["GET"])
def show_form():
    return render_template("form.html", employees=employees, edit_employee=None)

# PROSES FORM  ->  POST /employees/new (CREATE)
@employee_bp.route("/employees/new", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    position = request.form.get("position", "Staff")
    salary = request.form.get("salary", 0)

    if not name:
        return "Nama wajib diisi!", 400

    new_id = max([e["id"] for e in employees], default=0) + 1
    new = {
        "id": new_id,
        "name": name,
        "position": position,
        "salary": int(salary) if salary else 0,
    }
    employees.append(new)

    return redirect("/employees/new")


# --- FITUR UPDATE (EDIT) ---
@employee_bp.route("/employees/edit/<int:id>", methods=["GET"])
def edit_form(id):
    employee_to_edit = None
    for e in employees:
        if e["id"] == id:
            employee_to_edit = e
            break
    
    if not employee_to_edit:
        return "Employee tidak ditemukan", 404

    return render_template("form.html", employees=employees, edit_employee=employee_to_edit)


@employee_bp.route("/employees/update/<int:id>", methods=["POST"])
def update_employee(id):
    name = request.form.get("name")
    position = request.form.get("position", "Staff")
    salary = request.form.get("salary", 0)

    for e in employees:
        if e["id"] == id:
            e["name"] = name
            e["position"] = position
            e["salary"] = int(salary) if salary else 0
            break

    return redirect("/employees/new")


# --- FITUR DELETE (HAPUS) ---
@employee_bp.route("/employees/delete/<int:id>", methods=["POST", "GET"])
def delete_employee(id):
    global employees
    employees = [e for e in employees if e["id"] != id]
    return redirect("/employees/new")