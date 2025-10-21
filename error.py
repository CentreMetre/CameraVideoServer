import logging
import os
from datetime import datetime

from flask import jsonify, request, redirect, url_for


def log_uncaught_error(e):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"errors/uncaught_error/{timestamp}.log"

    logger = logging.getLogger(filename)
    logger.setLevel(logging.ERROR)


def log_error(e, note=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    directory = "logs/error"
    filename = os.path.join(directory, f"{timestamp}.log")

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    logger = logging.getLogger(filename)
    logger.setLevel(logging.ERROR)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    note_print = ""

    if note != "":
        note_print = f"Note:\n{note}\n\n=========\nNote Over\n=========\n"

    logger.error(f"{note_print}{e}", exc_info=True)

    logger.removeHandler(file_handler)


"""
===================
HTTP ERROR HANDLERS
===================
"""


def handle_404(e, description=""):
    if not description:
        description = f"Resource at {request.path} was not found."
    return jsonify({"error": e.name, "code": e.code, "description": description}), 404


"""
====================
FLASK ERROR HANDLERS
====================
"""


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        log_error(e)
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def handle_flask_exp_404(e):
        handle_404(e)

    @app.errorhandler(NotAuthedError)
    def handle_not_authed(e):
        # Needed instead of just 'login' because of blueprints
        return redirect(url_for("user.get_login_page", reason="noAuth"))


"""
====================
CUSTOM ERROR CLASSES
====================
"""


class NotAuthedError(Exception):
    def __init__(self, message, status_code=401):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
