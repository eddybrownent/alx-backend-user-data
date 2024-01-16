#!/usr/bin/env python3
"""
Basic authentication for API
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic auth that inherits from Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Gets Base64 part of Auth header for a Basic Authe
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_credentials = authorization_header[6:]
        return base64_credentials

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Gets the decoded value of a Base64 string
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decoded_value
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extracts Basic - User credentials
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_pass = decoded_base64_authorization_header.split(
                ':', 1)
        return user_email, user_pass

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Gets User instance based on email and password
        """
        if user_email is None or not isinstance(
                user_email,
                str) or user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if len(users) <= 0:
            return None

        user_instance = users[0] if isinstance(users, list) else users

        if not user_instance.is_valid_password(user_pwd):
            return None

        return user_instance
