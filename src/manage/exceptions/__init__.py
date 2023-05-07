from flask import abort
import logging


class Error(Exception):
    def __init__(self, message):
        logging.error(message)
        self.message = message
        self.error()

    def error(self):
        abort(404, description=self.message)
