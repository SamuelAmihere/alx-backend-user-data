#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List


def extract(fd: str,
            sep: str) -> str:
    """returns the value of a field in a message"""
    return r'(?P<field>{})=[^{}]*'.format('|'.join(fd), sep)


def replace(red: str) -> str:
    """returns the pattern to replace"""
    return r'\g<field>={}'.format(red)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(extract(fields, separator),
                  replace(redaction), message)
