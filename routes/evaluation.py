from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
import jwt
from config import SECRET_KEY
from auth import authorize_role
from db import mysql
import logging
from MySQLdb.cursors import DictCursor

eval_bp = Blueprint("eval", __name__)


@eval_bp.route("/<int:subject_id>", methods=["POST"])
@authorize_role(['coordinator'])
def addmarkscheme(subject_id):
    data = request.get_json()
    theory = data.get("theory", None)
    lab = data.get("lab", None)
    IA1 = data.get("ia1", None)
    IA2 = data.get("ia2", None)

    query = "INSERT INTO evaluation_scheme (theory_weightage, lab_weightage, ia1_weightage, ia2_weightage, subject_id) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (theory, lab, IA1, IA2, subject_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Scheme added successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@eval_bp.route("/scheme", methods=["POST"])
@authorize_role(['admin', 'coordinator'])
def addeval():
    data = request.get_json()
    subject_id = data.get("subject_id")
    group_id = data.get("group_id")
    course_id = data.get("course_id")
    staff_id = data.get("staff_id")
    start = data.get("start")
    till = data.get("till")

    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(
            "SELECT student_id FROM students WHERE group_id=%s", (group_id,))
        students = cursor.fetchall()

        if not students:
            return jsonify(create_error_response("No students found for the given group_id"))

        query = "INSERT INTO marksentry (student_id, subject_id, group_id, staff_id, from_date, till_date, course_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        for student in students:
            student_id = student['student_id']
            cursor.execute(query, (student_id, subject_id,
                           group_id, staff_id, start, till, course_id))

        mysql.connection.commit()
        cursor.close()

        return jsonify(create_success_response("Scheme added successfully for all students"))
    except Exception as e:
        logging.error(f"Error inserting scheme: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@eval_bp.route("/<course_name>", methods=["GET"])
@authorize_role(['coordinator'])
def getschemebycoursename(course_name):
    query = " select * from evaluation_scheme join subjects on evaluation_scheme.subject_id = subjects.subject_id join courses on subjects.course_id = courses.course_id where courses.course_name = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_name,))
        students = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(students))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@eval_bp.route("/getscheme/<course_name>", methods=["GET"])
@authorize_role(['coordinator'])
def getschemes(course_name):
    query = "SELECT marksentry.*, courses.course_name FROM marksentry JOIN courses ON marksentry.course_id = courses.course_id WHERE courses.course_name = %s"

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (course_name,))
        marks_entries = cursor.fetchall()
        cursor.close()

        result = []
        columns = ['entry_id', 'student_id', 'subject_id', 'group_id', 'course_id', 'staff_id',
                   'theory', 'lab', 'IA1', 'IA2', 'from_date', 'till_date', 'approved', 'course_name']

        for row in marks_entries:
            entry = dict(zip(columns, row))
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT student_name FROM students WHERE student_id = %s", (entry['student_id'],))
            student = cursor.fetchone()
            cursor.close()
            entry['student_name'] = student[0] if student else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT subject_name FROM subjects WHERE subject_id = %s", (entry['subject_id'],))
            subject = cursor.fetchone()
            cursor.close()
            entry['subject_name'] = subject[0] if subject else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT staff_name FROM staff WHERE staff_id = %s", (entry['staff_id'],))
            staff = cursor.fetchone()
            cursor.close()
            entry['staff_name'] = staff[0] if staff else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT group_name FROM course_groups WHERE group_id = %s", (entry['group_id'],))
            group = cursor.fetchone()
            cursor.close()
            entry['group_name'] = group[0] if group else None

            result.append(entry)

        return jsonify(create_success_response(result))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@eval_bp.route("/getschemestaff/<staff_id>", methods=["GET"])
@authorize_role(['staff'])
def getschemestaff(staff_id):
    query = "SELECT * FROM marksentry where approved = 0 and staff_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (staff_id,))
        marks_entries = cursor.fetchall()
        cursor.close()

        result = []
        columns = ['entry_id', 'student_id', 'subject_id', 'group_id', 'course_id',
                   'staff_id', 'theory', 'lab', 'IA1', 'IA2', 'from_date', 'till_date', 'approved']

        for row in marks_entries:
            entry = dict(zip(columns, row))
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT student_name FROM students WHERE student_id = %s", (entry['student_id'],))
            student = cursor.fetchone()
            cursor.close()
            entry['student_name'] = student[0] if student else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT subject_name FROM subjects WHERE subject_id = %s", (entry['subject_id'],))
            subject = cursor.fetchone()
            cursor.close()
            entry['subject_name'] = subject[0] if subject else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT staff_name FROM staff WHERE staff_id = %s", (entry['staff_id'],))
            staff = cursor.fetchone()
            cursor.close()
            entry['staff_name'] = staff[0] if staff else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT group_name FROM course_groups WHERE group_id = %s", (entry['group_id'],))
            group = cursor.fetchone()
            cursor.close()
            entry['group_name'] = group[0] if group else None

            result.append(entry)

        return jsonify(create_success_response(result))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@eval_bp.route("/getschemestaffapproved/<staff_id>", methods=["GET"])
@authorize_role(['staff'])
def getschemestaffcompleted(staff_id):
    query = "SELECT * FROM marksentry where approved = 1 and staff_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (staff_id,))
        marks_entries = cursor.fetchall()
        cursor.close()

        result = []
        columns = ['entry_id', 'student_id', 'subject_id', 'group_id', 'course_id',
                   'staff_id', 'theory', 'lab', 'IA1', 'IA2', 'from_date', 'till_date', 'approved']

        for row in marks_entries:
            entry = dict(zip(columns, row))
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT student_name FROM students WHERE student_id = %s", (entry['student_id'],))
            student = cursor.fetchone()
            cursor.close()
            entry['student_name'] = student[0] if student else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT subject_name FROM subjects WHERE subject_id = %s", (entry['subject_id'],))
            subject = cursor.fetchone()
            cursor.close()
            entry['subject_name'] = subject[0] if subject else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT staff_name FROM staff WHERE staff_id = %s", (entry['staff_id'],))
            staff = cursor.fetchone()
            cursor.close()
            entry['staff_name'] = staff[0] if staff else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT group_name FROM course_groups WHERE group_id = %s", (entry['group_id'],))
            group = cursor.fetchone()
            cursor.close()
            entry['group_name'] = group[0] if group else None

            result.append(entry)

        return jsonify(create_success_response(result))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@eval_bp.route("editmarks/<int:entry_id>", methods=["PUT"])
@authorize_role(['coordinator', 'staff'])
def editmarks(entry_id):
    data = request.get_json()
    theory = data.get("theory")
    lab = data.get("lab")
    IA1 = data.get("ia1")
    IA2 = data.get("ia2")

    query = "UPDATE marksentry set theory=%s, lab=%s, IA1=%s, IA2=%s where entry_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (theory, lab, IA1, IA2, entry_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Marks updated successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@eval_bp.route("approve/<int:entry_id>", methods=["PUT"])
@authorize_role(['coordinator'])
def approve(entry_id):
    data = request.get_json()
    approved = data.get("approved")

    query = "UPDATE marksentry set approved=%s where entry_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (approved, entry_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Approved successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@eval_bp.route("/approvedmarks/<course_name>", methods=["GET"])
@authorize_role(['coordinator'])
def getschemestaffapproved(course_name):
    # query = "SELECT * FROM marksentry where approved = 1"
    query = """SELECT marksentry.*, courses.course_name 
FROM marksentry 
JOIN courses ON marksentry.course_id = courses.course_id 
WHERE courses.course_name = %s 
  AND marksentry.approved = 1;"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (course_name,))
        marks_entries = cursor.fetchall()
        cursor.close()

        result = []
        columns = ['entry_id', 'student_id', 'subject_id', 'group_id', 'course_id', 'staff_id',
                   'theory', 'lab', 'IA1', 'IA2', 'from_date', 'till_date', 'approved', 'course_name']

        for row in marks_entries:
            entry = dict(zip(columns, row))
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT student_name FROM students WHERE student_id = %s", (entry['student_id'],))
            student = cursor.fetchone()
            cursor.close()
            entry['student_name'] = student[0] if student else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT subject_name FROM subjects WHERE subject_id = %s", (entry['subject_id'],))
            subject = cursor.fetchone()
            cursor.close()
            entry['subject_name'] = subject[0] if subject else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT staff_name FROM staff WHERE staff_id = %s", (entry['staff_id'],))
            staff = cursor.fetchone()
            cursor.close()
            entry['staff_name'] = staff[0] if staff else None

            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT group_name FROM course_groups WHERE group_id = %s", (entry['group_id'],))
            group = cursor.fetchone()
            cursor.close()
            entry['group_name'] = group[0] if group else None

            result.append(entry)

        return jsonify(create_success_response(result))
    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))
