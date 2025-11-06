from db.database import get_db_connection, commit_query, get_db_con_from_short_date
from media_types import MediaType

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
# is_downloaded (INTEGER) - Boolean (0 or 1) for storing if the file has been downloaded to the local machine/server.


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

    commit_query(con, insert_query)


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

    commit_query(con, update_query)


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

    commit_query(con, delete_query)

# Possible changes:
# Add get_db_connection for images so MediaType.IMAGE doesn't have to be used.