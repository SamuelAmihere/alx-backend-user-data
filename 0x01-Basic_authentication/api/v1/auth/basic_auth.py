#!/usr/bin/env python3
"""
BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User
import re


class BasicAuth(Auth):
    """BasicAuth class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 Authorization Header.
        """
        if authorization_header is None or \
           type(authorization_header) is not str:
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 Authorization Header.
        """
        if type(base64_authorization_header) == str:
            try:
                return base64.b64decode(
                    base64_authorization_header,
                    validate=True).decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the User Credentials.
        """
        if type(decoded_base64_authorization_header) == str:
            match_f = re.fullmatch(
                r'(?P<user>[^:]+):(?P<password>.+)',
                decoded_base64_authorization_header.strip())
            if match_f:
                usr = match_f.group('user')
                pwd = match_f.group('password')
                return (usr, pwd)
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password.
        """
        if type(user_pwd) == str and type(user_email) == str:
            try:
                user = {'email': user_email}
                users = User.search(user)
            except Exception:
                return None
            if not users or len(users) == 0:
                return None
            if not users[0].is_valid_password(user_pwd):
                return None
            return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        user, pwd = self.extract_user_credentials(decoded_header)
        if user is None or pwd is None:
            return None
        return self.user_object_from_credentials(user, pwd)
