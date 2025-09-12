import logging
from datetime import datetime

from flask import jsonify, request


def log_uncaught_error(e):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"errors/uncaught_error/{timestamp}.log"

    logger = logging.getLogger(filename)
    logger.setLevel(logging.ERROR)


def log_error(e, note=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"errors/error/{timestamp}.log"

    logger = logging.getLogger(filename)
    logger.setLevel(logging.ERROR)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    note = f"Note:\n{note}\n\n\n" if True else ''
    logger.error(f"{note}{e}", exc_info=True)

    logger.removeHandler(file_handler)


"""
==============
ERROR HANDLERS
==============
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