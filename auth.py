from functools import wraps
from flask import request, jsonify
import jwt
from config import SECRET_KEY
from utils import create_error_response

def authorize_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify(create_error_response("missing authorization header")), 401

            token = auth_header.split(" ")[1]
            if not token:
                return jsonify(create_error_response("missing token")), 401

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                print("Decoded Token:", payload)
                user_role = payload.get("role")
                if user_role not in allowed_roles:
                    return jsonify(create_error_response("Access forbidden")), 403
            except jwt.ExpiredSignatureError:
                return jsonify(create_error_response("expired token")), 401
            except jwt.InvalidTokenError:
                return jsonify(create_error_response("invalid token")), 401

            return f(*args, **kwargs)
        return decorated_function
    return decorator
