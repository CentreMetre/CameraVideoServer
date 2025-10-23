import os
import sqlite3 as sql

from types import MediaType

# Don't import camera, for separation of concerns.

image_db_name = os.environ["RECDB"] = "recdata.db"
rec_db_name = os.environ["IMGDB"] = "imgdata.db"


def get_db_connection(date, media_type) -> sql.Connection:
    """
    Returns connection to a DB file.

    Creates a connection, and creates the file if it doesn't yet exist.

    Parameters
    ----------
    date: str
        The date of the media to get the DB connection for in the format of "yyyymmdd", e.g. 20251023.
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

    connection = sql.connect(f"{date}/{db}")

    return connection