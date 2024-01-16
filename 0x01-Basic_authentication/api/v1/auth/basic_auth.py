#!/usr/bin/env python3
"""
Basic authentication for API
"""
from api.v1.auth.auth import Auth
import base64


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
