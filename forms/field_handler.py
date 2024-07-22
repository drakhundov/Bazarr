import io
from typing import Dict

from PIL import Image

import caching
import server


class FieldHandler:
    # * STRING
    @staticmethod
    def check_string_from_update(upd: Dict) -> bool:
        return upd.get("message") is not None

    @staticmethod
    def get_string_from_update(upd: Dict):
        return upd["message"]

    # * NATURAL NUMBER
    @staticmethod
    def check_natural_num_from_update(upd: Dict) -> bool:
        return upd.get("message") is not None and upd["message"].isnumeric()

    @staticmethod
    def get_natural_num_from_update(upd: Dict):
        return int(upd["message"])

    # * PHOTO
    @staticmethod
    def check_photo_from_update(upd: Dict) -> bool:
        if not upd.get("file_id") is not None:
            return False
        file_id = server.get_file(upd["file_id"])
        image = caching.retrieve(caching.IMAGE, file_id)
        if image is not None:
            try:
                Image.open(io.BytesIO(image))
                return True
            except Exception:
                return False
        else:
            return False

    @staticmethod
    def get_photo_from_update(upd: Dict):
        if (photo := caching.retrieve(caching.IMAGE, upd["file_id"])) is not None:
            return photo
        return server.get_file(upd["file_id"])

    # * LOCATION
    @staticmethod
    def check_location_from_update(upd: Dict) -> bool:
        return upd.get("latitude") is not None and upd.get("longitude") is not None

    @staticmethod
    def get_location_from_update(upd: Dict):
        return (upd["latitude"], upd["longitude"])
