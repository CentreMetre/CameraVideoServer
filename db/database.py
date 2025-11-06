import os
import sqlite3 as sql

import util
from media_types import MediaType

# Don't import camera, for separation of concerns.

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


def commit_query(connection, query):
    """
    Util function to commit a query.

    Commits a query with a connection, and then closes the connection. Used for modifying data, not reading data.

    Parameters
    ----------
    connection:  sql.Connection
        The connection to the database.
    query: str
        The query to do on the database.
    """
    connection.execute(query)
    connection.commit()
    connection.close()

# CHOICES
# Camera should handle camera IO and importantly db file cleaning, not the test_database.py
# Make each functions open and close their own connections. Makes it safer so that the wrong connection isn't provided.
