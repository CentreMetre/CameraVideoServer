from enum import Enum


class VideoColumn(Enum):
    CAMERA = "on_camera"
    LOCAL_265 = "local_has_265"
    LOCAL_WRAPPED_265 = "local_has_wrapped_265"
    LOCAL_264 = "local_has_264"
