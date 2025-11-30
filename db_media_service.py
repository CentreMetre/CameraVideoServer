import db.image_db as image_db
import db.video_db as video_db

def image_get_all(date):
    """
    Retrieve all rows from the image DB for a specific date.

    Parameters
    ----------
    date: str
        The date of the media to retrieve from the DB for in the format of yyyymmdd, e.g. 20251023.
    Returns
    -------
    list:
        A list of tuples with the data. Tuple format: (file_name, path, is_downloaded)
    """
    return image_db.retrieve_all(date)


def video_get_all(date):
    """
    Retrieve all rows from the video DB for a specific date.

    Parameters
    ----------
    date: str
        The date of the media to retrieve from the DB for in the format of yyyymmdd, e.g. 20251023.
    Returns
    -------
    list:
        A list of tuples with the data. Tuple format: (file_name, path, is_downloaded)
    """
    return video_db.retrieve_all(date)

# def filter_image_after():
#     pass
#
#
# def filter_by_is_downloaded(date, filter_out: bool):
#     """
#     Filter rows out.
#
#     Return rows based on if they are downloaded.
#
#     Parameters
#     ----------
#     date: str
#         The date of the media to retrieve from the DB for in the format of yyyymmdd, e.g. 20251023.
#     filter_out: bool
#         The value of the is_downloaded column to filter out.
#         If filter_out is true is_downloaded is true, that row gets filtered out.
#
#     Returns
#     -------
#     List:
#         A list of tuples of the filtered rows. Tuple format: (file_name, path, is_downloaded)
#     """
#
#     rows = get_all(date)
#
#     for row in rows:
#         if row[2] == filter_out:
#             rows.remove(row)
#
#     return rows

# Choices:
# Filtering will be done on client
