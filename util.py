import os
from pathlib import Path

from flask import session, redirect, url_for, request

import camera
from bs4 import BeautifulSoup
from functools import wraps

from camera import download_and_process_database
from logger_conf import logger

from datetime import datetime

rec_db = os.getenv("RECDB")
img_db = os.getenv("IMGDB")
db_suffix = os.getenv("DBSUFFIX")


def get_current_dates_from_sd_page(html):
    """
    Gets the html from the camera. Gets all dates on the index page.

    Returns: List of dates in their original format of yyyymmdd (e.g. 20250718)
    """
    logger.debug(html)
    html = camera.get_index_page()
    soup = BeautifulSoup(html, 'html.parser')

    dates = []

    for a_tag in soup.find_all('a'):
        date_text = a_tag.get_text().strip()
        date_text = date_text.rstrip('/')  # Strips the trailing slash
        try:
            int(date_text)  # Test to see if it is a
            dates.append(date_text)
        except ValueError:
            continue

    return dates


def format_date(date):
    """
    Formats a date from a yyyymmdd format into a dd/mm/yyyy format

    date (string): the date to format

    Returns: the formatted date
    """
    year = date[:4]
    month = date[4:6]
    day = date[6:]

    new_date = f"{day}/{month}/{year}"

    return new_date


#   formatted_dates.append(new_date)

def format_dates(dates):
    """
    Formats dates from a yyyymmdd format into a dd/mm/yyyy format

    dates (list of strings): the dates to format

    Returns:
    list: the formatted dates
    """
    new_dates = []
    for date in dates:
        new_dates.append(format_date(date))
    return new_dates


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('credentials'):
            return redirect(url_for('login?redirected=true', next=request.url))
        return f(*args, **kwargs)

    return decorated


def load_file(file_path):
    """
    Loads a file from a given path.

    Parameters:
        file_path (str): the absolute path to the file.

    Returns: the loaded file in bytes.
    """
    with open(file_path, "rb") as f:
        data = f.read()

    return data


def create_abs_path(date, media_subfolder, file_name):
    """
    Create an absolute path for a file. Checks that the user input is secure to prevent directory traversal.
    """
    base_path = os.path.abspath("files")
    requested_path = os.path.abspath(os.path.join(base_path, date, media_subfolder, file_name))

    if not requested_path.startswith(base_path):
        raise ValueError("Invalid path: outside base directory")

    return requested_path


def write_media_file(date, media_subfolder, file_name, file_bytes):
    """
    Save a file to the server.

    Parameters:
        date (string): the date to save the file.
        media_subfolder (string): the subfolder to save the file.
        file_name (string): the name of the file.
        file_bytes (bytes): the bytes of the file.
    """
    logger.debug(f"Saving file of length {len(file_bytes)} to {date}/{media_subfolder}/{file_name}")

    local_path = f"files/{date}/{media_subfolder}/{file_name}"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(file_bytes)

    logger.debug(f"Wrote {len(file_bytes)} bytes to {local_path}")


def update_todays_database() -> None:
    formatted_date = datetime.now().strftime("%Y%m%d")

    dbs = ["rec", "img"] # fixed because it didnt = rec or img, but the whole db name. THe following functionc all requires the emdia type in img or rec

    for db in dbs:
        camera.download_and_process_database(formatted_date, db)


def load_database_file(date, data_media_name) -> list[str]:
    """
    Gets database server, processes it, and then stores it on the server in `files/{date}/recdata.db`.

    Parameters:
    date (string): The date of the database in the format of yyyymmdd.
    data_media_name (string): What database's contents to get. "rec" for the recording database and "img" for the image database.

    Return: A list of all file names found in the database.
    """
    if date == datetime.now().strftime("%Y%m%d"):
        update_todays_database()

    if data_media_name != "rec" and data_media_name != "img":
        raise ValueError("Database name must be 'rec' or 'img'. You inputted '" + data_media_name + "' instead.")

    file_path = Path(f"files/{date}/{data_media_name}{db_suffix}")
    if not file_path.exists():
        download_and_process_database(date, data_media_name)
    if file_path.exists():
        content = file_path.read_text()
        return content.split("\n")


def update_local_non_cam_databases() -> None:
    """
    Update all databases that are stored on the server from previous requests
    but not ones that are currently on the camera.
    """
    directory = "files"

    dates_server_stored = get_dir_names_in_directory(directory)

    camera_dates = get_current_dates_from_sd_page(camera.get_index_page())  # Current dates on the camera
    camera_dates.sort()  # Sort for past-most first date at top, just to make sure.

    earliest_cam_date = camera_dates[0]
    date_checking = dates_server_stored[0]

    dbs = [rec_db, img_db]

    # Example object:
    # files = {"20250901": {"record000": ["file1", "file2"], "record001": ["file1", "file2"]}}

    file_dict = {}

    for date in dates_server_stored:
        if int(date) >= int(earliest_cam_date):
            break  # Stop if the stored dates gets to the camera stored dates

        sub_folders = get_dir_names_in_directory(directory + f"/{date}")
        for sub in sub_folders:
            files = get_file_names_in_directory(directory + f"/{date}/{sub}")
            if files:  # only store non-empty lists
                file_dict.setdefault(date, {})[sub] = files

    write_locations_to_fresh_databases(file_dict)


def write_locations_to_fresh_databases(files:  dict[str, dict[str, list[str]]]) -> None:
    """
    Writes locations to a database file that is emptied and then written to.

    Parameters:
        files: dict[str, dict[str, list[str]]]: A dictionary of file names and file paths. Example:
        {"20250901": {"record000": ["file1", "file2"], "record001": ["file1", "file2"]}}

    """
    for date, subfolders in files.items():
        record_db_path = f"files/{date}/{rec_db}"
        image_db_path = f"files/{date}/{img_db}"
        with open(record_db_path, "w") as record_db, open (image_db_path, "w") as image_db:
            for subfolder, file_list in subfolders.items():
                if "record" in subfolder:
                    db = record_db
                if "image" in subfolder:
                    db = image_db
                else:
                    continue

                for file in file_list:
                    file_path = f"files/{date}/{subfolder}/{file}\n"
                    db.write(file_path)

def replace_line_in_database(file_path: str, line: str) -> None:
    if line[-3:] == "mp4":
        line_to_replace = line[:-3] + "265"

    file_lines = open(file_path, "r").readlines()

    # if file_lines.
    #
    # for line in file_lines:
    #
    # with open(file_path, "r") as file:

def get_file_names_in_directory(directory):
    file_names = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_names.append(file)

    return file_names


def get_dir_names_in_directory(directory):
    dir_names = []
    for folders in os.listdir(directory):
        path = os.path.join(directory, folders)
        if os.path.isdir(path):
            dir_names.append(folders)

    return dir_names

# wipe db file
# for directory in date, for file in directory, db write file.name
# date/subfolder/filename - db line structure
# Rename .mp4 to have .265 since elsewhere in code its designed to handle that


def extract_filename_from_path(filepath: str) -> str:
    """
    Extracts the filename from a given filepath, including extension.

    Parameters:
        filepath (str): The path to extract the filename from. The filename should be the last part of the path. Delimiters should be /

    Returns: The filename including the extension
    """
    parts = filepath.split("/")

    return parts[-1]
