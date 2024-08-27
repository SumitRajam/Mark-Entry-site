from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
import jwt
from config import SECRET_KEY
from db import mysql
import logging
from auth import authorize_role
from MySQLdb.cursors import DictCursor

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("", methods=["GET"])
@authorize_role(['admin', 'coordinator'])
def getstaff():
    query = "SELECT * FROM staff"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@staff_bp.route("/<course_name>", methods=["GET"])
@authorize_role(['coordinator'])
def getstaffbycoursename(course_name):
    query = "SELECT * FROM staff where course_name = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_name,))
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@staff_bp.route("/<int:staff_id>", methods=["PUT"])
@authorize_role(['admin'])
def staffcourse(staff_id):
    data = request.get_json()
    course_name = data.get("course_name")
    role = data.get("role")
    print(course_name, role)
    query = "UPDATE staff SET course_name = %s, role = %s WHERE staff_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_name, role, staff_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Staff course updated successfully"))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@staff_bp.route("/register", methods=["POST"])
def staffregister():
    data = request.get_json()
    name = data.get("staffname")
    email = data.get("staffemail")
    password = data.get("password")
    employee_number = data.get("employee_number")
    role = data.get("role")
    course_name = data.get("course_name")

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    query = "INSERT INTO staff (staff_name, email, password, role, course_name, employee_number) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (name, email, encrypted_password, role, course_name, employee_number))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("User registered successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@staff_bp.route("/login", methods=["POST"])
def stafflogin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Encrypt the password
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    query = "SELECT staff_id, staff_name, email, course_name, role FROM staff WHERE email = %s AND password = %s"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (email, encrypted_password))
        staff = cursor.fetchone()
        cursor.close()

        if not staff:
            return jsonify(create_error_response("User not found!"))

        # Create the payload with retrieved staff information
        payload = {
            "staff_id": staff[0],
            "staff_name": staff[1],
            "email": staff[2],
            "course_name": staff[3],
            "role": staff[4]
        }
        

        # Encode the payload to create the token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(create_success_response({"token": token, "user_name": staff[1]}))
    except Exception as e:
        return jsonify(create_error_response(str(e)))

