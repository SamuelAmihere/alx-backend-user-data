#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from typing import Tuple
import os
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST handler for login url:
    /api/v1/auth_session/login
    """
    user_email_err = {"error": "no user found for this email"}

    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        all_users = User.search({'email': email})
    except Exception:
        return jsonify(user_email_err), 404
    if len(all_users) <= 0:
        return jsonify(user_email_err), 404
    if all_users[0].is_valid_password(password):
        from api.v1.app import auth
        resp = jsonify(all_users[0].to_json())
        session_id = auth.create_session(getattr(
                            all_users[0], 'id'))
        resp.set_cookie(os.getenv("SESSION_NAME"),
                        session_id)
        return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE handler for logout url:
    /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
