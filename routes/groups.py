from flask import Blueprint, request, jsonify
from utils import create_success_response, create_error_response
import hashlib
import jwt
from config import SECRET_KEY
from db import mysql
import logging
from auth import authorize_role
from MySQLdb.cursors import DictCursor

group_bp = Blueprint("group", __name__)

@group_bp.route("", methods=["GET"])
def allgroups():
    query = "SELECT * FROM course_groups"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query)
        groups = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(groups))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@group_bp.route("/<int:course_id>", methods=["GET"])
@authorize_role(['admin', 'coordinator', 'staff'])
def getgroups(course_id):
    query = "SELECT * FROM course_groups where course_id = %s"
    try:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute(query, (course_id,))
        groups = cursor.fetchall()
        cursor.close()
        return jsonify(create_success_response(groups))
    except Exception as e:
        logging.error(f"Error fetching courses: {str(e)}")
        return jsonify(create_error_response(f"Database error: {str(e)}"))


@group_bp.route("", methods=["POST"])
@authorize_role(['admin'])
def addgroup():
    data = request.get_json()
    group_name = data.get("group_name")
    course_id = data.get("course_id")

    query = "INSERT INTO course_groups (group_name, course_id) VALUES (%s, %s)"
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            query, (group_name, course_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify(create_success_response("Group added successfully"))
    except Exception as e:
        return jsonify(create_error_response(str(e)))