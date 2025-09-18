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

    return render_template("index.html")


@app.route("/api/dates")
def get_dates():
    cam_index = camera.get_index_page()
    dates = util.get_current_dates_from_sd_page(cam_index)

    return jsonify(dates), 200


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

    database = util.load_database_file(date, media_type)
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
        file, file_ready = video.handle_video_request(date, media_subfolder, file_name)
        mime_type = "video/mp4"
        file_name = file_name[:-3] + "mp4"  # Change extension to MP4 since it is now an MP4
    if file_type == "jpg":  # Handles image file requests
        file = image.handle_image_request(date, media_subfolder, file_name)
        mime_type = "image/jpeg"
        file_ready = True
    if file_type != "265" and file_type != "jpg":
        return jsonify({"error": "Invalid file type. 'jpg' or '265' are required"}), 400

    if file_ready:
        if action == "view":
            return send_file(file,
                             mimetype=mime_type)
        if action == "download":
            return send_file(file,
                             mimetype=mime_type,
                             as_attachment=True,
                             download_name=file_name)

    if not file_ready:
        return jsonify({"message": "Video is found and exists but is being encoded."}), 202

@app.route("/search")
def search():
    """
    Gets all videos that currently exist in the given date and time range. If no optional parameters are passed,
    all results are returned. If a date is passed without the time, the search is started from the start of the day/
    stopped at the end of the day. If only times are provided, evey day is included within those times.
    This will provide results for media stored both on the camera and on this server.

    Example: domain.tld/search?start-date=20250901&start-time=1543&end-date=20250901&end-time=1946

    Parameters:
        start-date (str): Start date in YYYYMMDD (optional).
        start-time (str): Start time in HHMM (optional).
        end-date (str): End date in YYYYMMDD (optional).
        end-time (str): End time in HHMM (optional).
    """
    start_date = request.args.get("start_date", "19000101")  # Second param is default
    end_date = request.args.get("end_date", "29991231")
    start_time = request.args.get("start_time", "0000")
    end_time = request.args.get("end_time", "1199")





os.makedirs("files/", exist_ok=True)
app.run(debug=is_debug)
error.register_error_handlers(app)
# TODO: Have to encode, browsers cant play mp4 wrapped 265
# TODO: Handle if a video file has 999999 the end time, that indicates its not finished recording yet.
# TODO: Have the ability to view after wrapping, then encode if download is requested.
# TODO: Add these to readme
