#!/usr/bin/env python3
"""
"""
import logging
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str):
    """
    func using regex to replace occur of certain field values
    """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
