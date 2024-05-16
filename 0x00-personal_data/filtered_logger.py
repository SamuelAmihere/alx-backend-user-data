#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List


def pattern(separator, fields, redaction, message):
    fn1 = lambda x, y: r'(?<=' + x + r'=).*?(?=' + y + r')'
    replace = lambda x: re.sub(
        fn1(x, separator),
        redaction, message)
    return '|'.join(map(replace, fields))


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    return re.sub(pattern(
        separator,
        fields,
        redaction,
        message), redaction, message)
