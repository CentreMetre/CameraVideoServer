import os
import sqlite3 as sql

from types import MediaType

# Don't import camera, for separation of concerns.

# Database example for imgdata db:
# +=====================+=====================+===============+
# |      file_name      |      location       | is_downloaded |
# +=====================+=====================+===============+
# | A25102006312300.jpg | 20251020/images000/ | True          |
# +---------------------+---------------------+---------------+
# | A25102006312300.jpg | 20251020/images000/ | False         |
# +---------------------+---------------------+---------------+
# file_name (TEXT) - The name of the file.
# location (TEXT) - The location of the file, excluding the filename.
# is_downloaded (INTEGER) - Boolean (0 or 1) for storing whether the file has been downloaded to the local machine/server.

# Database example for recdata db (best so far):
# +=======================+===========+===============+=======================+===============+=====================+
# |       base_name       | on_camera | local_has_265 | local_has_wrapped_265 | local_has_264 |        path         |
# +=======================+===========+===============+=======================+===============+=====================+
# | P251020_000000_001000 | True      | False         | True                  | True          | 20251020/record000/ |
# +-----------------------+-----------+---------------+-----------------------+---------------+---------------------+
# base_name (TEXT) - Stores the filename without the extension.
# on_camera (INTEGER) - Boolean (0 or 1) for storing whether the file still exists on the camera (files get deleted automatically for space constraints).
# local_has_265 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server in unencoded H.265/HEVC format.
# local_has_wrapped_265 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server in the wrapped (NOT encoded) form (H.265 in MP4).
# local_has_264 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server in the encoded form (H.264).
# path (TEXT) - The relative path up to the file from the servers working directory, e.g. 20251028/images000/

rec_db_name = os.environ["RECDB"] = "recdata.db"
image_db_name = os.environ["IMGDB"] = "imgdata.db"


def get_db_connection(date, media_type) -> sql.Connection:
    """
    Returns connection to a DB file.

    Creates a connection, and creates the file if it doesn't yet exist.

    Parameters
    ----------
    date: str
        The date of the media to get the DB connection for in the format of yyyymmdd, e.g. 20251023.
    media_type: MediaType
        Enum indicating the media type.

    Returns
    -------
    sqlite3.Connection
        The connection to the DB file.
    """

    # db = "" # Not needed because of implicit declaration

    if media_type == MediaType.IMAGE:
        db = image_db_name
    else:
        db = rec_db_name

    os.makedirs(f"files/{date}", exist_ok=True)

    connection = sql.connect(f"files/{date}/{db}")

    return connection


def init_db(date, media_type):
    """
    Create an SQLite DB file.

    Creates an SQLite DB file for eiter images or videos on a specific date.

    Parameters
    ----------
    date: str
        The date of the media to create the DB for in the format of yyyymmdd, e.g. 20251023.
    media_type: MediaType
        Enum indicating the media type.
    """

    create_image_table = """
    create table images (
      file_name TEXT,
      location TEXT,
      is_downloaded BOOLEAN
    );
    """

    create_video_table = """"""

    # Getting connection this way is safer since it reduces the risk of the user initialising the DB in the wrong file,
    # but less modular/DRY.
    con = get_db_connection(date, media_type)
    cur = con.cursor()

    # os.makedirs not needed since that's done in connection creation.
    # os.makedirs(f"files/{date}")

    if media_type == MediaType.IMAGE:
        cur.execute(create_image_table)
    else:
        cur.execute(create_video_table)


def insert_image_row(connection, full_path):
    """
    Inserts a row in an image DB.

    Inserts and populates a row in the image DB for the provided connection with the file name and location.

    Parameters
    ----------
    connection: sqlite3.Connection
        The connection to the SQLite database.

    full_path: string
        The full path of the image file. E.g. 20251020/images000/A25102006312300.jpg
    """

    path_sections = full_path.split("/")

    date = path_sections[-3]

    file_name = path_sections[-1]

    # Done like this incase "sd" is prepended
    location = f"{date}/{path_sections[-2]}"


# CHOICES
# Camera should handle camera IO and importantly db file cleaning, not the test_database.py
# Make user provide connection. Makes it so this doesn't have to get the date from the file name. That can be got easier.
