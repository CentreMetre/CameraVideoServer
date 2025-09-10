import camera
import util
from pathlib import Path


def handle_image_request(date, media_subfolder, file_name):
    """
    Handles the request for a video. Saves it if it doesn't exist on server.
    """
    requested_path = util.create_abs_path(date, media_subfolder, file_name)
    if not Path(requested_path).exists():
        image_file = camera.download_file(date, media_subfolder, file_name)  # Split from at and unpack for variables
        util.write_media_file(date, media_subfolder, file_name, image_file)

    jpg_file = util.load_file(requested_path)
    return jpg_file
