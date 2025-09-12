from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from logger_conf import logger
import base64, util
import requests
import os
import re

import error

load_dotenv()

cam_url = os.getenv("CAMERA_SD_URL")
rec_db = os.getenv("RECDB")
img_db = os.getenv("IMGDB")
db_suffix = os.getenv("DBSUFFIX")


def get_index_page():
    """
    Returns: The HTML of the index page.
    """
    response = requests.get(cam_url, headers=util.get_headers(), stream=True)
    return response.text


def download_and_process_database(date, data_media_name):
    """
    Gets the recording database from the camera, processes it, and then stores it on the server in `files/{date}/recdata.db`.

    Parameters:
    date (string): The date of the database in the format of yyyymmdd.
    data_media_name (string): What database to download and process. "rec" for the recording database and "img" for the image database.

    Return: The path the database was stored to. It should be `files/{date}/{database_name}data.db`.
    """

    file_type = ""

    if data_media_name != "rec" and data_media_name != "img":
        raise ValueError("Database name must be 'rec' or 'img'")

    if data_media_name == "rec":
        file_type = "265"
    if data_media_name == "img":
        file_type = "jpg"

    rec_db_url = f"{cam_url}/{date}/{data_media_name}data.db"

    try:
        response = requests.get(rec_db_url, util.get_headers())
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if date in get_index_page():
            error.handle_404(e, f"Even though {date} is reported as being on the camera, "
                                f"the database could not be downloaded.")
            error.log_error(e, note=f"Even though {date} is reported as being on the camera, "
                                    f"the database could not be downloaded.")
        raise Exception(404)  # (e, note=f"That date doesn't exist on the camera.")

    file_bytes = response.content

    print(file_bytes)

    lines = process_database_bytes(file_bytes, file_type)
    print(lines)
    file_path = f"files/{date}/{data_media_name}data.db"  # Keep as DB, so it's the same as the camera
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a") as f:
        for line in lines:
            f.write(line + "\n")

    return file_path


def process_database_bytes(database_bytes, file_type):
    """
    Processes the database bytes and returns a list of the strings.

    Parameters:
        database_bytes (bytes): The bytes of the database file.
        file_type (string): What type of file to process, should be either "jpg" or "265".

    Return: The list of strings.
    """

    file_type = file_type.lstrip(".")

    pattern = ""

    if file_type != "265" and file_type != "jpg":
        raise ValueError("Unsupported file type. Should be jpg or 265")

    if file_type == "jpg":
        pattern = re.compile(rb'(sd/.*?\.jpg)')
    if file_type == "265":
        pattern = re.compile(rb'(sd/.*?\.265)')

    matches = re.findall(pattern, database_bytes)

    sd_stripped_matches = []

    for s in matches:
        s = s.decode('ascii')
        sd_stripped_matches.append(s[3:])  # Removes sd/ in matches

    return sd_stripped_matches


def load_database_file(date, data_media_name):
    """
    Gets database server, processes it, and then stores it on the server in `files/{date}/recdata.db`.

    Parameters:
    date (string): The date of the database in the format of yyyymmdd.
    data_media_name (string): What database's contents to get. "rec" for the recording database and "img" for the image database.

    Return: A list of all file names found in the database.
    """
    if data_media_name != "rec" and data_media_name != "img":
        raise ValueError("Database name must be 'rec' or 'img'. You inputted '" + data_media_name + "' instead.")

    file_path = Path(f"files/{date}/{data_media_name}{db_suffix}")
    if not file_path.exists():
        download_and_process_database(date, data_media_name)
    if file_path.exists():
        content = file_path.read_text()
        return content.split("\n")


def download_file(date, media_subfolder, file_name):
    """
    Downloads the file from the camera.

    Parameters:
        date (string): The date of the database in the format of yyyymmdd.
        media_subfolder (string): What subfolder to download the images from, e.g. record000 or images000.
        file_name (string): What file to download.
    """

    address = f"{cam_url}/{date}/{media_subfolder}/{file_name}"
    logger.debug(f"Calling {address} to download file")
    response = requests.get(address, util.get_headers())
    logger.debug(f"Finished Downloading.")
    if response.status_code != 200:
        raise Exception(f"Couldnt get file off camera. Status code: {response.status_code}")
    return response.content
