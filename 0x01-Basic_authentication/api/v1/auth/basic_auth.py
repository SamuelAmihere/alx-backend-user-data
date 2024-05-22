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
