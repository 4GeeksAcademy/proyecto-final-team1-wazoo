from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get("roles", [])
            user_active = claims.get("is_active", False)
            if not any(role in roles for role in user_roles):
                return jsonify({"msg": "Access forbidden: insufficient permissions"}), 403
            if not user_active:
                return jsonify({"msg": "Access forbidden: user is inactive"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator