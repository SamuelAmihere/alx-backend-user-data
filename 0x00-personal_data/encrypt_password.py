#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text
in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
