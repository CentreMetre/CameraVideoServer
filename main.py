import subprocess

from flask import Flask, render_template, jsonify, send_file

import video
from user import user_bp
from dotenv import load_dotenv
import camera
import util
import os

load_dotenv()
secret_key = os.getenv("USER_SECRET_KEY")
db_suffix = os.getenv("DBSUFFIX")
is_debug = os.getenv("IS_DEBUG")

app = Flask(__name__)
app.secret_key = secret_key
app.register_blueprint(user_bp)


@app.route("/")
def index():
    cam_index = camera.get_index_page()
    dates = util.format_dates(util.get_current_dates_from_sd_page(cam_index))

    return render_template("index.html", items=dates)


@app.route("/<date>/<media_type>")
def get_media_list_from_date(date, media_type):
    """
    Gets the specified media type from the specified date.

    Parameters:
        date (str): The date to get the specified media type from.
        media_type (str): The type of media to get. "rec" for video recordings, "img" for images.

    Returns: JSON of just a list with all file names in separate elements.
    """
    if media_type != "rec" and media_type != "img":
        return jsonify({"error": "Invalid media type. 'rec' or 'img' are required."}), 400

    database = camera.load_database_file(date, media_type)
    return jsonify(database)


@app.route("/<date>/<media_subfolder>/<file_name>/<action>")
def get_file(date, media_subfolder, file_name, action):
    """
    Gets the specified file from the specified date and location.
    """
    if action != "view" and action != "download":
        return jsonify({"error": "Invalid action. 'view' or 'download' are required"}), 400

    base_path = os.path.abspath("files")
    requested_path = os.path.abspath(os.path.join(base_path, date, media_subfolder, file_name))
    requested_mp4_path = requested_path[:-3]
    requested_mp4_path += "mp4"

    if not requested_path.startswith(base_path):
        return jsonify({"error": "Illegal traversal"}), 403

    if not os.path.isfile(requested_mp4_path):
        file = camera.download_file(date, media_subfolder, file_name)
        file_path = video.wrap_265_with_mp4_and_save(date, media_subfolder, file_name, file)
        # video.write_media_file(date, media_subfolder, file_name, file)
        # TODO: Write file if its a jpg

    file = open(requested_mp4_path, "rb")

    if file_name.endswith("jpg"):
        mime_type = "image/jpeg"

    if file_name.endswith("265"):
        mime_type = "video/mp4"

    if action == "view":
        return send_file(file,
                         mimetype=mime_type)

    if action == "download":
        return send_file(file,
                         mimetype=mime_type,
                         as_attachment=True,
                         download_name=file_name)

    # if action == "view":
    #     return send_file(f"files/{date}/{media_subfolder}/{file_name}",
    #                      mimetype=mime_type)
    #
    # if action == "download":
    #     return send_file(f"files/{date}/{media_subfolder}/{file_name}",
    #                      mimetype=mime_type,
    #                      as_attachment=True,
    #                      download_name=file_name)


app.run(debug=is_debug)

# TODO: Have to encode, browsers cant play mp4 wrapped 265