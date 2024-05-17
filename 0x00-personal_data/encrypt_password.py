#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text
in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns a salted, hashed password """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check valid password """
    return bcrypt.checkpw(password.encode(), hashed_password)
