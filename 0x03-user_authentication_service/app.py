#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """
    return a JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    End-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, "message": "user created"})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    login function to respond to the POST /sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')
    login_info = AUTH.valid_login(email, password)

    if login_info:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    If user exists destroy session & redirect user to GET
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Retrieve user profile based on provided session ID

    Returns:
        JSON: User profile or 403 status
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        profile = {"email": user.email}
        return jsonify(profile), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generates reset password token for user of the givev email

    Returns:
        JSON: Reset password token or 403 status if email is not
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
