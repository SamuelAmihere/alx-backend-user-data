#!/usr/bin/env python3
"""
BasicAuth
"""
from api.v1.auth.auth import Auth


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
        if user_email is None or type(user_email) is not str or \
           user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None
