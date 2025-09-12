import os

from flask import session, redirect, url_for, request

import camera
from bs4 import BeautifulSoup
from functools import wraps


def get_current_dates_from_sd_page(html):
    """
    Gets the html from the camera. Gets all dates on the index page.

    Returns: List of dates in their original format of yyyymmdd (e.g. 20250718)
    """
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


def get_headers():
    """
    Returns: object of the headers needed for requests
    """
    encoded_credentials = session.get('credentials')
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }
    return headers


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
    local_path = f"files/{date}/{media_subfolder}/{file_name}"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(file_bytes.content)

