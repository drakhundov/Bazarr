from typing import Dict

from forms.field_types import *


class Field:
    def __init__(self, title: str, field_metadata: Dict, prompt: str):
        self.title = title
        for attr, val in field_metadata.items():
            setattr(self, attr, val)
        self.prompt = prompt
        self.value = None

    def check_update_validity(self, upd: Dict) -> bool:
        return self.check_from_update_func(upd)

    def parse_from_update(self, upd: Dict):
        return self.get_from_update_func(upd)

    def __str__(self):
        return self.title
