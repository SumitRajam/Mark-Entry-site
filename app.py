from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from utils import create_success_response, create_error_response
from config import SECRET_KEY, PORT_NO
import jwt
from db import init_db
from routes.routes import user_bp, default
from routes.evaluation import eval_bp
from routes.subject import subject_bp
from routes.courses import course_bp
from routes.groups import group_bp
from routes.staff import staff_bp

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)

mysql = init_db(app)

# Return version
@app.route("/version", methods=["GET"])
def version():
    return jsonify(create_success_response("1.0"))


# Middleware for protected routes
# @app.before_request
# def require_authorization():
#     skip_urls = ["/user/student/login", "/user/student/register", "/version", "/user/students", "/user/test_db", "/user/staff/register"]
#     if request.path in skip_urls:
#         return None

#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         return jsonify(create_error_response("missing authorization header")), 401

#     token = auth_header.split(" ")[1]
#     if not token:
#         return jsonify(create_error_response("missing token")), 401
    
#     try:
#         payload =jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         request.data = payload
#     except jwt.ExpiredSignatureError:
#         return jsonify(create_error_response("Expired token")), 401
#     except jwt.InvalidTokenError:
#         return jsonify(create_error_response("Invalid token")), 401
    
#Add Routes

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(default, url_prefix="")
app.register_blueprint(eval_bp, url_prefix="/eval")
app.register_blueprint(subject_bp, url_prefix="/subject")
app.register_blueprint(course_bp, url_prefix="/course")
app.register_blueprint(group_bp, url_prefix="/group")
app.register_blueprint(staff_bp, url_prefix="/staff")

if __name__ == "__main__":
    app.run(port=PORT_NO, debug=True)