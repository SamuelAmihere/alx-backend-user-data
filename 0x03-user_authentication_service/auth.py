#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password

    Args:
        password (str): The password to hash

    Returns:
        bytes: The hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
