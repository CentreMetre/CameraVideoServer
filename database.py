import os
import sqlite3 as sql

from types import MediaType

# Don't import camera, for separation of concerns.

# Database example for imgdata db:
# +=====================+========================================+===============+
# |      file_name      |                location                | is_downloaded |
# +=====================+========================================+===============+
# | A25102006312300.jpg | 20251020/images000/A25102006312300.jpg | True          |
# +---------------------+----------------------------------------+---------------+
# | A25102006312300.jpg | 20251020/images000/A25102006573600.jpg | False         |
# +---------------------+----------------------------------------+---------------+

# Database example for recdata db:
# +===========================+===========================+===========================+=====================+
# |     camera_file_name      |   local_file_unencoded    |    local_file_encoded     |        path         |
# +===========================+===========================+===========================+=====================+
# | NULL                      | P251020_000000_000000.265 | P251020_000000_000000.mp4 | 20251020/record000/ |
# +---------------------------+---------------------------+---------------------------+---------------------+
# | P251020_000000_001000.265 | P251020_000000_001000.265 | P251020_000000_001000.mp4 | 20251020/record000/ |
# +---------------------------+---------------------------+---------------------------+---------------------+
# | P251020_001000_002000.265 | P251020_001000_002000.265 | NULL                      | 20251020/record000/ |
# +---------------------------+---------------------------+---------------------------+---------------------+
# | P251020_005001_010001.265 | NULL                      | NULL                      | 20251020/record000/ |
# +---------------------------+---------------------------+---------------------------+---------------------+
# (This example is not exhaustive of the possible combinations on a row. Any combination is possible, as long as path is
# populated if any of the other columns are populated)
# camera_file_name - The name of the file on the camera. NULL if its no longer on the camera.
# local_file_unencoded - The name of the file that has been downloaded but not encoded.
# local_file_encoded - The name of the file that has been.
# path - The path upto, and excluding, the filename. Is the same on local or the camera.

# Database example 2 for recdata db:
# +===========================+===========================+==============+=========================+=====================+
# |      file_unencoded       |       file_encoded        | is_on_camera | is_downloaded_unencoded |        path         |
# +===========================+===========================+==============+=========================+=====================+
# | P251020_010001_011001.265 | P251020_010001_011001.mp4 | True         | True                    | 20251020/record000/ |
# +---------------------------+---------------------------+--------------+-------------------------+---------------------+
# file_unencoded - text - Filename of the unencoded file.
# file_encoded - text - Filename of the encoded file.
# is_on_camera - boolean - If the file is still on the camera or not.
# is_downloaded_unencoded

# Database example 3 for recdata db (best so far):
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

# Camera should handle camera IO and importantly db file cleaning, not the database.py
