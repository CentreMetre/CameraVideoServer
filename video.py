from logger_conf import logger
import subprocess
import os
import tempfile
from pathlib import Path

import camera
import util
from logger_conf import logger


def encode_265_to_264_mp4_and_save(date, media_subfolder, file_name, h265_bytes, force_overwrite=False):
    """
    Encodes an h265 video file to h264 and wraps it in mp4.


    """

    logger.debug(f"In encode function.")

    base_path = "files"
    mp4_file_name = file_name[:-3]
    mp4_file_name += "mp4"
    output_path = os.path.abspath(os.path.join(base_path, date, media_subfolder, mp4_file_name))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    tmp_path = output_path + ".tmp"

    command = [
        "ffmpeg",
        "-f", "hevc",              # input format: raw H.265/HEVC
        "-i", "pipe:0",            # read from stdin
        "-c:v", "libx264",         # encode to H.264
        "-preset", "fast",          # optional: encoding speed/efficiency
        "-pix_fmt", "yuv420p",
        "-f", "mp4", # Ensures its outputted to mp4
        "-y" if force_overwrite else "-n",  # overwrite if force else no overwrite
        tmp_path
    ]

    logger.debug("Encoding video.")
    process = subprocess.run(command, input=h265_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.debug("Finished encoding.")

    if process.returncode != 0:
        logger.error(f"FFmpeg encoding failed: {process.stderr.decode()}")
        if Path(tmp_path).exists():
            Path(tmp_path).unlink()  # Deletes file if it exists but failed.
        raise RuntimeError(f"FFmpeg encoding failed: {process.stderr.decode()}")

    Path(tmp_path).rename(output_path)

    return output_path

def wrap_265_with_mp4_and_save(date, media_subfolder, file_name, h265_bytes):
    """
    Wraps a raw h265 video file with an mp4 container. Saves it to the server.

    Parameters:
        date (string): The date of the video in format of yyyymmdd.
        media_subfolder (string): The subfolder where the video will be saved, e.g. record000 or record001.
        file_name (string): The name of the video file, consists of <A | P><date>_<start time>_<end time>.265.
        h265_bytes (bytes): The raw 265 video file.

    Return (string): The location of the written mp4 file.
    """

    base_path = "files"
    mp4_file_name = file_name[:-3]  # Remove 265 off the file name
    mp4_file_name += "mp4"
    output_path = os.path.abspath(os.path.join(base_path, date, media_subfolder, mp4_file_name))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".265", delete=False) as temp_input:
        temp_input.write(h265_bytes)
        temp_input_path = temp_input.name

    print("at ffmpeg try")

    try:
        # FFmpeg command
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", temp_input_path,
            "-c:v", "copy",  # copy video
            "-c:a", "aac",  # convert audio if present
            "-strict", "experimental",
            output_path  # final MP4 path
        ]
        # Run FFmpeg
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode())
    finally:
        # Delete temporary H.265 file
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)

    return mp4_file_name


def handle_video_request(date, media_subfolder, file_name):
    """
    Handles the request for a video. Saves it if it doesn't exist on server.
    """
    is_ready = True
    requested_path = util.create_abs_path(date, media_subfolder, file_name)
    requested_mp4_path = requested_path[:-3]
    requested_mp4_path += "mp4"
    if not Path(requested_mp4_path).exists():
        logger.debug(f"Path: {requested_mp4_path} not found.")
        video_file = camera.download_file(date, media_subfolder, file_name)
        encode_265_to_264_mp4_and_save(date, media_subfolder, file_name, video_file)
        is_ready = True

    if Path(requested_mp4_path + ".tmp").exists():
        is_ready = False

    # Make it return the file path instead of the file since flask can load and send it easier.
    return requested_mp4_path, is_ready

