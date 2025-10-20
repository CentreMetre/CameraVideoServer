from flask import Flask, jsonify, send_file, request, send_from_directory, session
import secrets

from logger_conf import logger

import error
import image
import video
from user import user_bp
import camera
import util
import os

os.environ["USER_SECRET_KEY"] = secrets.token_hex(32)
# os.environ["IMGDB"] = "imgdata.db"
# os.environ["RECDB"] = "recdata.db"
# os.environ["DBSUFFIX"] = "data.db"

secret_key = os.getenv("USER_SECRET_KEY")
db_suffix = os.getenv("DBSUFFIX")

print(f"secret key: {os.getenv('USER_SECRET_KEY')}")
print(f"db suffix: {os.getenv('DBSUFFIX')}")
print(f"imgdb name: {os.getenv('IMGDB')}")
print(f"recdb name: {os.getenv('RECDB')}")

is_debug = os.getenv("IS_DEBUG")
print(is_debug)
if is_debug != "False" and is_debug != "True":
    print(f"IS_DEBUG is not a known value of {is_debug}. Defaulting to False.")
    is_debug = False

if is_debug == "True":
    is_debug = True
if is_debug == "False":
    is_debug = False

is_dev = os.getenv("IS_DEV")
print(is_dev)
if is_dev != "False" and is_dev != "True":
    print(f"IS_DEBUG is not a known value of {is_debug}. Defaulting to False.")
    is_dev = False

if is_dev == "True":
    is_dev = True
if is_dev == "False":
    is_dev = False

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.secret_key = secret_key
app.register_blueprint(user_bp)
error.register_error_handlers(app)


@app.route("/")
def index():
    cam_index = camera.get_index_page()
    dates = util.format_dates(util.get_current_dates_from_sd_page(cam_index))

    return send_from_directory("static/pages", "date-list.html")


@app.route("/api/dates")
def get_dates():
    cam_index = camera.get_index_page()
    dates = util.get_current_dates_from_sd_page(cam_index)



    return jsonify(dates), 200


@app.route("/api/<date>/<media_type>")
def get_media_list_from_date_and_type(date, media_type):
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


@app.route("/api/<date>/filenames")
def get_media_filenames_from_date(date):
    """
    Gets all media from specified date.

    Parameters:
        date (str): The date to get the media list from

    Returns: JSON of a list of media file names.
    """
    img_list = util.load_database_file(date, "img")

    img_filenames = []

    for img in img_list:
        img_filenames.append(util.extract_filename_from_path(img))

    rec_list = util.load_database_file(date, "rec")

    rec_filenames = []

    for rec in rec_list:
        rec_filenames.append(util.extract_filename_from_path(rec))

    full_list = img_filenames + rec_filenames

    logger.debug(full_list)

    return jsonify(full_list)


@app.route("/api/<date>/paths")
def get_media_paths_from_date(date):
    """
    Gets all media from specified date.

    Parameters:
        date (str): The date to get the media list from

    Returns: JSON of a list of media file names.
    """
    img_list = util.load_database_file(date, "img")

    rec_list = util.load_database_file(date, "rec")

    full_list = img_list + rec_list

    return jsonify(full_list)


@app.route("/date/<date>")
def serve_date_page(date):
    return send_from_directory("static/pages", "media-list.html")


@app.route("/file/<date>/<media_subfolder>/<file_name>/<action>")
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

    # TODO: implement returning a page for when video view/download is requested, then show progress if possible using web sockets

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


@app.route("/favicon.ico")
def get_favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route("/test")
def test():
    return os.getenv("USER_SECRET_KEY")

print(f"is_debug: {is_debug}")
print(f"is_dev: {is_dev}")


os.makedirs("files/", exist_ok=True)
if is_dev:
    if(is_debug):
        print(os.environ)
    print("Running Flask App")
    app.run(debug=is_debug)

# TODO: Have to encode, browsers cant play mp4 wrapped 265
# TODO: Handle if a video file has 999999 the end time, that indicates its not finished recording yet.
# TODO: Have the ability to view after wrapping, then encode if download is requested.
# TODO: Add these to readme
# TODO: Create "amount of images/videos" endpoint, that returns the amount for a given date. Or could just count when retrieved for showing the media
# TODO: Refactor to use send_from_directory for 0 Server Side Rendering. Do it in user.py as well
# TODO: Change DB writing/handling so there Isn't empty new lines at the end.
# TODO: Idea: Have auth be if not authed throw an error for easier redirection. Only need to check on some APIs, might be easier
# TODO: Implement viewing a wrapped instead of encuded file, but have a warning if its wrapped. Also have buttons for deleting files.
# Auth check notes: only need to check on api calls, not page serving, so that would make it easier to check for auth
