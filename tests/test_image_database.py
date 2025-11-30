# test_image_database.py
# Written with AI, replace asap.
import os
import sqlite3
import tempfile
from unittest import mock
import pytest

import db.image_db as image_db
from db import database as db
from media_types import MediaType  # your own media_types.py


@pytest.fixture(autouse=True)
def temp_dir(monkeypatch):
    """Redirect file operations to a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.chdir(tmp)
        yield


@pytest.fixture
def mock_util(monkeypatch):
    """Mock util.convert_short_date_to_long_date_ISO."""
    mocked = mock.Mock(return_value="20251020")
    monkeypatch.setattr(db, "util", mock.Mock(convert_short_date_to_long_date_ISO=mocked))
    return mocked


def test_get_db_connection_creates_file_and_dir():
    con = db.get_db_connection("20251020", MediaType.IMAGE)
    con.close()

    assert os.path.exists("files/20251020/imgdata.db")


def test_get_db_con_from_short_date_uses_util_conversion(mock_util):
    con = db.get_db_con_from_short_date("A25102006312300.jpg", MediaType.IMAGE)
    con.close()

    mock_util.assert_called_once_with("A25102006312300.jpg")
    assert os.path.exists("files/20251020/imgdata.db")


def test_init_db_creates_images_table():
    db.init_db("20251020", MediaType.IMAGE)

    con = sqlite3.connect("files/20251020/imgdata.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='images';")
    assert cur.fetchone() is not None
    con.close()


def test_insert_image_row_adds_entry():
    date = "20251020"
    db.init_db(date, MediaType.IMAGE)

    path = f"{date}/images000/A25102006312300.jpg"
    os.makedirs(f"files/{date}/images000", exist_ok=True)
    image_db.insert_image_row(path)

    con = sqlite3.connect(f"files/{date}/imgdata.db")
    cur = con.cursor()
    cur.execute("SELECT file_name, path, is_downloaded FROM images;")
    row = cur.fetchone()
    assert row == ("A25102006312300.jpg", f"{date}/images000", 0)
    con.close()


def test_update_image_downloaded_updates_value(mock_util):
    date = "20251020"
    db.init_db(date, MediaType.IMAGE)

    path = f"{date}/images000/A25102006312300.jpg"
    os.makedirs(f"files/{date}/images000", exist_ok=True)
    image_db.insert_image_row(path)

    image_db.update_image_downloaded("A25102006312300.jpg", True)

    con = sqlite3.connect(f"files/{date}/imgdata.db")
    cur = con.cursor()
    cur.execute("SELECT is_downloaded FROM images;")
    value = cur.fetchone()[0]
    print("test_update_image_downloaded_updates_value")
    print(value)
    assert value == 1
    con.close()


def test_delete_image_row_removes_entry(mock_util):
    date = "20251020"
    db.init_db(date, MediaType.IMAGE)

    path = f"{date}/images000/A25102006312300.jpg"
    os.makedirs(f"files/{date}/images000", exist_ok=True)
    image_db.insert_image_row(path)

    image_db.delete_image_row("A25102006312300.jpg")

    con = sqlite3.connect(f"files/{date}/imgdata.db")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM images;")
    count = cur.fetchone()[0]
    assert count == 0
    con.close()

def test_get_all_image_rows(mock_util):
    date = "20251020"
    db.init_db(date, MediaType.IMAGE)

    paths = [f"{date}/images000/A25102006312300.jpg", f"{date}/images000/A25102006312400.jpg"]
    os.makedirs(f"files/{date}/images000", exist_ok=True)
    for path in paths:
        image_db.insert_image_row(path)

    expected = [(f"A25102006312300.jpg", f"{date}/images000", 0), (f"A25102006312400.jpg", f"{date}/images000", 0)]

    rows = image_db.retrieve_all(date)
    assert rows == expected
    print(rows)