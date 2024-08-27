from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
import jwt
from config import SECRET_KEY
from db import mysql
import logging
from auth import authorize_role
from MySQLdb.cursors import DictCursor

subject_bp = Blueprint("subject", __name__)

@subject_bp.route("", methods=["GET"])
def subjects():
    query = "SELECT * FROM subjects"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        subjects = cursor.fetchall()
        cursor.close()

        return jsonify(create_success_response(subjects))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@subject_bp.route("/<int:course_id>", methods=["GET"])
@authorize_role(['admin', 'coordinator'])
def subject(course_id):
    query = "SELECT * FROM subjects where course_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_id,))
        subjects = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(subjects))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))
    
@subject_bp.route("/<course_name>", methods=["GET"])
@authorize_role(['coordinator'])
def subjectcoursename(course_name):
    query = "SELECT * FROM subjects join courses on subjects.course_id = courses.course_id left join evaluation_scheme on subjects.subject_id = evaluation_scheme.subject_id where courses.course_name = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_name,))
        subjects = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(subjects))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@subject_bp.route("", methods=["POST"])
@authorize_role(['admin'])
def addsubject():
    data = request.get_json()
    subject_name = data.get("subject_name")
    course_id = data.get("course_id")

    query = "INSERT INTO subjects (subject_name, course_id) VALUES (%s, %s)"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (subject_name, course_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Subject added successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@subject_bp.route("/<int:subject_id>", methods=["PUT"])
def updatesubject(subject_id):
    data = request.get_json()
    subject_name = data.get("subject_name")
    course_id = data.get("course_name")

    query = "UPDATE subjects SET subject_name = %s, course_id = %s WHERE subject_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (subject_name, course_id, subject_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Course updated successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@subject_bp.route("/<int:subject_id>", methods=["DELETE"])
def deletesubject(subject_id):
    query = "DELETE FROM subjects WHERE subject_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (subject_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Course deleted successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))