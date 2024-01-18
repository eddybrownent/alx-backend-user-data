#!/usr/bin/env python3
"""
Authentication system
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if auth is required for given path

        Args:
            path : path to check for auth
            exluded_paths : list of paths that are excluded from authe

        Returns:
            bool - True if authe is required else false
        """
        if path is None or excluded_paths is None:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                base_excluded_path = excluded_path.rstrip('*')
                if path.startswith(base_excluded_path):
                    return False
            elif path == excluded_path or path + '/' ==\
                    excluded_path or path.rstrip('/') == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Generates the authe header for the Flask Request

        Args:
            request: Flask request object

        Returns:
            str - the auth header generated
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets current user based on the Flask request

        Args:
            request: Flask request object

        Returns:
            TypeVar('User') : Current user
        """
        return None
