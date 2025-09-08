import subprocess
import os
import tempfile

def wrap_265_with_mp4_and_save(date, media_subfolder, file_name, h265_bytes):
    """
    Wraps a raw h265 video file with an mp4 container.

    Parameters:
        video (bytes): The raw 265 video file.

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
            "-c:v", "copy",       # copy video
            "-c:a", "aac",        # convert audio if present
            "-strict", "experimental",
            output_path           # final MP4 path
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

def write_media_file(date, media_subfolder, file_name, file_bytes):
    local_path = f"files/{date}/{media_subfolder}/{file_name}"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(file_bytes.content)