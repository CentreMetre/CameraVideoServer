import os
import sqlite3 as sql

from types import MediaType

import util

# Don't import camera, for separation of concerns.

# Database example for imgdata db:
# +=====================+=====================+===============+
# |      file_name      |      location       | is_downloaded |
# +=====================+=====================+===============+
# | A25102006312300.jpg | 20251020/images000/ | True          |
# +---------------------+---------------------+---------------+
# | A25102006312300.jpg | 20251020/images000/ | False         |
# +---------------------+---------------------+---------------+
# NOTE: Existence of an image row indicated if the file is available on the camera, no separate column of that.
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

    # Makes dirs only
    os.makedirs(f"files/{date}", exist_ok=True)

    # Makes file if it doesn't exist
    connection = sql.connect(f"files/{date}/{db}")

    return connection

def get_db_con_from_short_date(date, media_type) -> sql.Connection :
    """
    Returns connection to a DB file using a short cam date.

    Creates a connection, and creates the file if it doesn't yet exist.

    Parameters
    ----------
    short_date: str
        The date of the media to get the DB connection for in the format of any string accepted by
        util.convert_short_date_to_long_date_ISO. E.g. a full filename could be provided.
    media_type: MediaType
        Enum indicating the media type.

    Returns
    -------
    sqlite3.Connection
        The connection to the DB file.
    """
    date = util.convert_short_date_to_long_date_ISO(date)
    return get_db_connection(date, media_type)

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

    con.close()


def insert_image_row(full_path):
    """
    Inserts a row in an image DB.

    Inserts and populates a row in the image DB for the provided connection with the file name and location.

    Parameters
    ----------
    full_path: str
        The full path of the image file. E.g. 20251020/images000/A25102006312300.jpg
    """

    path_sections = full_path.split("/")

    date = path_sections[-3]

    con = get_db_connection(date, MediaType.IMAGE)

    file_name = path_sections[-1]

    # Done like this incase "sd" is prepended
    location = f"{date}/{path_sections[-2]}"

    insert_query = f"""
    INSERT INTO images (file_name, location, is_downloaded)
    VALUES ('{file_name}', '{location}', false);
    """ # is_downloaded is False by default because this is creating the row and no media is downloaded yet.

    con.execute(insert_query)

    con.close()


def update_image_downloaded(file_name, value):
    """
    Update if the image is downloaded in the DB.

    Parameters
    ----------
    file_name: str
        The filename of the row to update. E.g. A25102006312300.jpg
    value: bool
        The value to change is_downloaded to.
    """

    con = get_db_con_from_short_date(file_name, MediaType.IMAGE)

    update_query = f"""
    update images set is_downloaded = {value};
    """

    con.execute(update_query)

    con.close()

def delete_image_row(file_name):
    """
    Delete a row from the DB.

    Deletes a row from the DB, used if the file is no longer existent on the cam or locally.

    Parameters
    ----------
    file_name: str
        The filename of the row to delete. E.g. A25102006312300.jpg
    """

    con = get_db_con_from_short_date(file_name, MediaType.IMAGE)

    delete_query = f"""
    DELETE FROM images where file_name is '{file_name}';
    """

    con.execute(delete_query)

    con.close()

# CHOICES
# Camera should handle camera IO and importantly db file cleaning, not the test_database.py
# Make each functions open and close their own connections. Makes it safer so that the wrong connection isn't provided.
