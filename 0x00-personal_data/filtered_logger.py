#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List


def extraxt(field: str, message: str,
            separator: str) -> str:
    """returns the value of a field in a message"""
    return re.search(f'{field}=(.*?){separator}',
                     message).group(1)


def pattern(fields: List[str], separator: str) -> str:
    """returns the pattern for the regex"""
    return f'({separator.join(fields)})=(.*?){separator}'


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(pattern(fields, separator),
                  lambda x: f'{x.group(1)}={redaction}',
                  message)
