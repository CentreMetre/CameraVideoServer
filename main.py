from flask import Flask, render_template, jsonify, send_file, request

import error
import image
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
        return jsonify({"error": f"Invalid action. 'view' or 'download' are required, but {action} was provided."}), 400

    file_type = file_name[-3:]

    requested_path = util.create_abs_path(date, media_subfolder, file_name)

    if file_type == "265":  # Handles video file requests
        file = video.handle_video_request(date, media_subfolder, file_name)
        mime_type = "video/mp4"
        file_name = file_name[:-3] + "mp4"  # Change extension to MP4 since it is now an MP4
    if file_type == "jpg":  # Handles image file requests
        file = image.handle_image_request(date, media_subfolder, file_name)
        mime_type = "image/jpeg"
    if file_type != "265" and file_type != "jpg":
        return jsonify({"error": "Invalid file type. 'jpg' or '265' are required"}), 400

    if action == "view":
        return send_file(file,
                         mimetype=mime_type)
    if action == "download":
        return send_file(file,
                         mimetype=mime_type,
                         as_attachment=True,
                         download_name=file_name)


app.run(debug=is_debug)
error.register_error_handlers(app)
# TODO: Have to encode, browsers cant play mp4 wrapped 265
