#!/usr/bin/env python3
"""
1. Regex-ing
"""
import re
from typing import List
import os
import logging
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    return mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        port=3306)


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


def main():
    """connects to the secure database
    and log all rows in the users table
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"

    query = "SELECT {} FROM users".format(fields)

    logger = get_logger()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        msg = "; ".join(
            [f"{fields.split(',')[i]}={row[i]}"
             for i in range(len(fields.split(',')))])
        log = logging.LogRecord(
            'user_data',
            logging.INFO,
            None,
            None,
            msg,
            None,
            None)
        logger.handle(log)

    cursor.close()


if __name__ == '__main__':
    main()
