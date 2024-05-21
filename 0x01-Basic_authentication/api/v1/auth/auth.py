#!/usr/bin/env python3
"""
The authentication module.
"""
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """The authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """The require_auth method.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """The authorization_header method.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """The current_user method.
        """
        return None
