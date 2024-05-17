#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    SEPARATOR = ";"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Redacting Formatter class """
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR)
        return super().format(record)


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
