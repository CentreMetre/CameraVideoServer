from bs4 import BeautifulSoup
from dotenv import load_dotenv
import base64, util
import requests
import os
import re

load_dotenv()

cam_url = os.getenv("CAMERA_SD_URL")
rec_db = os.getenv("RECDB")
img_db = os.getenv("IMGDB")


def get_index_page():
    """
    Returns: The HTML of the index page.
    """
    response = requests.get(cam_url, headers=util.get_headers(), stream=True)
    return response.text


def download_and_process_database(date, database_name):
    """
    Gets the recording database from the camera, processes it, and then stores it on the server in `files/{date}/recdata.db`.

    Parameters:
    date (string): The date of the database in the format of yyyymmdd.
    database_name (string): What database to download and process. "rec" for the recording database and "img" for the image database.

    Return: The path the database was stored to. It should be `files/{date}/{database_name}data.db`.
    """

    file_type = ""

    if database_name != "rec" and database_name != "img":
        raise ValueError("Database name must be 'rec' or 'img'")

    if database_name == "rec":
        file_type = "265"
    if database_name == "img":
        file_type = "jpg"

    rec_db_url = f"{cam_url}/{date}/{database_name}data.db"
    response = requests.get(rec_db_url, util.get_headers())
    response.raise_for_status()

    file_bytes = response.content

    lines = process_database_bytes(file_bytes, file_type)

    file_path = f"files/{date}/{database_name}data.txt"

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
        sd_stripped_matches.append(s[3:]) # Removes sd/ in matches

    return sd_stripped_matches

"""
    D
"""