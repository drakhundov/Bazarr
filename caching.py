from typing import Type

_cache = {"images": {}}

IMAGE = 1
BUILT_IN_TYPE = {
    IMAGE: bytes
}


def cache(cache_type: int, value, _id: int):
    if not isinstance(value, BUILT_IN_TYPE[cache_type]):
        raise TypeError(f"caching.cache: value must be of {cache_type} type.")
    if cache_type == IMAGE:
        _cache["images"][_id] = value


def retrieve(cache_type: int, _id: int):
    if cache_type == IMAGE:
        return _cache["images"].get(_id)
    