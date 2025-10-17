import base64
import os
import requests

from flask import session, jsonify, request, Blueprint, redirect, url_for, send_from_directory

from logger_conf import logger

url = os.getenv("CAMERA_SD_URL")

user_bp = Blueprint('user', __name__)


@user_bp.route("/login", methods=['GET'])
def get_login_page():
    return send_from_directory("static/pages", "login.html")


@user_bp.route("/auth/login", methods=['POST'])
def auth_user():
    if not request.form["username"] or not request.form["password"]:
        return jsonify({"Error": "Missing or invalid JSON"}), 400

    username = request.form["username"]
    password = request.form["password"]

    encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        session['credentials'] = encoded_credentials
        return redirect(url_for("index"))

    return redirect(url_for("user.get_login_page", redirect="true"))
