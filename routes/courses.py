from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
from auth import authorize_role
import jwt
from config import SECRET_KEY
from db import mysql
import logging
from MySQLdb.cursors import DictCursor

course_bp = Blueprint("course", __name__)


@course_bp.route("/", methods=["GET"])
@authorize_role(['admin', 'coordinator', 'staff'])
def courses():
    query = "SELECT * FROM courses"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        courses = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(courses))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@course_bp.route("", methods=["POST"])
@authorize_role(['admin'])
def addcourse():
    data = request.get_json()
    course_name = data.get("course_name")
    description = data.get("description", "")

    query = "INSERT INTO courses (course_name, description) VALUES (%s, %s)"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (course_name, description))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Course added successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@course_bp.route("/<int:course_id>", methods=["PUT"])
@authorize_role(['admin'])
def updatecourse(course_id):
    data = request.get_json()
    course_name = data.get("course_name")
    description = data.get("description", "")

    query = "UPDATE courses SET course_name = %s, description = %s WHERE course_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (course_name, description, course_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Course updated successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))


@course_bp.route("/<int:course_id>", methods=["DELETE"])
@authorize_role(['admin'])
def deletecourse(course_id):
    query = "DELETE FROM courses WHERE course_id = %s"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, (course_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Course deleted successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))
