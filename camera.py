from bs4 import BeautifulSoup
from dotenv import load_dotenv
import base64, util
import requests, dotenv, os

load_dotenv()

url = os.getenv("CAMERA_SD_URL")


def get_index_page():
    """
    Returns: The HTML of the index page.
    """
    response = requests.get(url, headers=util.get_headers())
    return response.text


def get_databases(date):
    response = requests.get(url + date, util.get_headers)