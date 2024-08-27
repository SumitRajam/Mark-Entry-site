from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
import jwt
from config import SECRET_KEY
from db import mysql
from auth import authorize_role
import logging
from MySQLdb.cursors import DictCursor

user_bp = Blueprint("user", __name__)
default = Blueprint("/", __name__)


@user_bp.route("/student/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    roll = data.get("roll")
    password = data.get("password")

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    query = "INSERT INTO students (student_name, email, roll_number,password) VALUES (%s, %s, %s, %s)"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (name, email, roll, encrypted_password))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("User registered successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@user_bp.route("/student/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    query = "SELECT student_id, student_name, email FROM students WHERE email = %s AND password = %s"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (email, encrypted_password))
        student = cursor.fetchone()
        cursor.close()

        if not student:
            return jsonify(create_error_response("User not found!"))

        payload = {
            "student_id": student[0],
            "student_name": student[1],
            "email": student[2]
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify(create_success_response({"token": token, "student_name": student[1]}))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@user_bp.route("/students", methods=["GET"])
def students():
    query = "SELECT * FROM students"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/assigncourse", methods=["GET"])
@authorize_role(['admin'])
def studentsnocourse():
    query = "SELECT * FROM students WHERE course_id IS NULL"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/assigngroup", methods=["GET"])
@authorize_role(['staff'])
def studentsnogroup():
    query = "SELECT * FROM students WHERE group_id IS NULL"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/havegroup", methods=["GET"])
@authorize_role(['staff'])
def studentsgroup():
    query = "SELECT * FROM students WHERE group_id IS NOT NULL"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/<int:course_id>", methods=["GET"])
@authorize_role(['admin'])
def studentsbycourse(course_id):
    query = "SELECT * FROM students WHERE course_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_id,))
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/assigncourse/<int:student_id>", methods=["PUT"])
def addCourse(student_id):
    data = request.get_json()
    course_id = data.get("course_id")
    query = "UPDATE students SET course_id = %s WHERE student_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_id, student_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Student course updated successfully"))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/assigngroup/<int:student_id>", methods=["PUT"])
@authorize_role(['admin', 'staff'])
def addGroup(student_id):
    data = request.get_json()
    course_id = data.get("group_id")
    query = "UPDATE students SET group_id = %s WHERE student_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_id, student_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Student group updated successfully"))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/students/removegroup/<int:roll_number>", methods=["PUT"])
@authorize_role(['staff'])
def remove_group(roll_number):
    try:
        query = "UPDATE students SET group_id = NULL WHERE roll_number = %s"
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (roll_number,))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Student group removed successfully"))
    except Exception as e:
        logging.error(f"Error removing group: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))

@user_bp.route("/students/course", methods=["GET"])
def students_in_entry():
    try:
        cursor = mysql.connection.cursor(DictCursor)

        cursor.execute("SELECT course_id FROM courses WHERE course_name = %s")
        students = cursor.fetchall()

        # cursor.execute(query, (course_id, course_id))
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@user_bp.route("/studentmarks/<int:student_id>", methods=["GET"])
def studentmarks(student_id):
    try:
        cursor = mysql.connection.cursor(DictCursor)

        cursor.execute("SELECT students.student_name, students.group_id, marksentry.subject_id, marksentry.theory, marksentry.lab, marksentry.IA1, marksentry.IA2 FROM students JOIN marksentry ON students.student_id = marksentry.student_id WHERE students.student_id = %s and approved = 1", (student_id,))
        students = cursor.fetchall()
        cursor.close()
        result = []
        columns = ['student_name', 'group_id', 'subject_id', 'theory', 'lab', 'IA1', 'IA2']
        for row in students:
            entry = dict(zip(columns, row.values()))

            cursor = mysql.connection.cursor(DictCursor)
            cursor.execute("SELECT group_name FROM course_groups WHERE group_id = %s", (entry['group_id'],))
            group_name = cursor.fetchone()
            cursor.close()
            entry['group_name'] = group_name['group_name'] if group_name else None

            cursor = mysql.connection.cursor(DictCursor)
            cursor.execute("SELECT subject_name FROM subjects WHERE subject_id = %s", (entry['subject_id'],))
            subject_name = cursor.fetchone()
            cursor.close()
            entry['subject_name'] = subject_name['subject_name'] if subject_name else None

            result.append(entry)

        return jsonify(create_success_response(result))
    except Exception as e:
        logging.error(f"Error fetching marks: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))
