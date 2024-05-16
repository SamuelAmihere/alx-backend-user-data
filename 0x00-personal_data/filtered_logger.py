#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    fn1 = lambda x, y: r'(?<=' + x + r'=).*?(?=' + y + r')'
    replace = lambda x: re.sub(fn1(x, separator), redaction, message)

    for field in fields:
        replace(field)
