#!/usr/bin/env python3
"""
script to hash a given password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates random salt and hash the password
    """
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
