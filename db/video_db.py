from db.database import get_db_connection, commit_query, get_db_con_from_short_date, init_db
from media_types import MediaType
from db import video_column


# Database example for recdata db (best so far):
# Table name: videos
# +=======================+===========+===============+=======================+===============+=====================+
# |       base_name       | on_camera | local_has_265 | local_has_wrapped_265 | local_has_264 |        path         |
# +=======================+===========+===============+=======================+===============+=====================+
# | P251020_000000_001000 | True      | False         | True                  | True          | 20251020/record000/ |
# +-----------------------+-----------+---------------+-----------------------+---------------+---------------------+
# base_name (TEXT) - Stores the filename without the extension.
# ====
# on_camera (INTEGER) - Boolean (0 or 1) for storing whether the file still exists on the camera (files get deleted
# automatically by the cam on the cam when space fills).
# ====
# local_has_265 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server in
# unencoded H.265/HEVC format.
# ====
# local_has_wrapped_265 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server
# in the wrapped (NOT encoded) form (H.265 in MP4).
# ====
# local_has_264 (INTEGER) - Boolean (0 or 1) for storing whether the file exists on the local machine/server
# in the encoded form (H.264).
# ====
# path (TEXT) - The relative path up to the file from the servers working directory, e.g. 20251028/images000/
#
# Note: If all are false, the row should be deleted since the file isn't available any more at all.


def init_video_db(date):
    """
    Create an SQLite DB file.

    Creates an SQLite DB file for videos on a specific date.

    Parameters
    ----------
    date: str
        The date of the media to create the DB for in the format of yyyymmdd, e.g. 20251023.
    """

    init_db(date, MediaType.VIDEO)


def insert_video_row(full_path):
    """
    Inserts a row in a video DB.

    Inserts and populates a row, with some default values, in the video DB for provided file name and path.
    The default values are:

    on_camera = true | local_has_265 = false | local_has_wrapped_265 = false | local_has_264 = false

    Parameters
    ----------
    full_path: str
    The full path of the image file. E.g. 20251020/record000/P251020_000000_001000.265
    """
    path_sections = full_path.split("/")

    date = path_sections[-3]

    con = get_db_connection(date, MediaType.VIDEO)

    file_name = path_sections[-1]
    base_name = file_name.split(".")[0]

    # Done using [-x] incase sd is prepended.
    location = f"{date}/{path_sections[-2]}"

    insert_query = f"""
    INSERT INTO videos (base_name, on_camera, local_has_265, local_has_wrapped_265, local_has_264, path)
    VALUES ('{file_name}', true, false, false, false, '{location}');
    """ # true, false, false, false done by default because it is assumed that the file is on the camera when creating
        # the DB, and isn't downloaded yet to the server in any form.

    commit_query(con, insert_query)

def update_video_row(base_name, to_update):
    """
    Updates a video rows stored data info.

    Updates the on_camera, local_has_265, local_has_wrapped_265, and local_has_264 rows to show where the video
    is stored and how.

    Parameters
    ----------
    base_name: string
        The name of the file to update the info on. Can be the base name.
        E.g. P251020_000000_001000.265 or P251020_000000_001000
    to_update: dict[video_column.VideoColumn, bool]
        A dict that stores the column to update and the value to update it to,
    """

    con = get_db_con_from_short_date(base_name, MediaType.VIDEO)

    for key in to_update:
        query = f"""
        update videos set {key.value} = {to_update[key]} where base_name is '{base_name}';
        """
        commit_query(con, query)


def retrieve_all(date):
    """
    Retrieve all rows from a specific date.

    Parameters
    ----------
    date: str
        The date of the media to retrieve from the DB for in the format of yyyymmdd, e.g. 20251023.

    Returns
    -------
    list:
        A list of tuples with the data. Tuple format: (file_name, path, is_downloaded)
    """

    con = get_db_connection(date, MediaType.IMAGE)

    cur = con.cursor()
    rows = cur.fetchall()

    return rows
