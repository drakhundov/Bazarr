from typing import Any, Callable, Dict, List

import server

from forms.field import Field


class Form:
    def __init__(self, fields: List, process_form_callback: Callable[[int, int], None]):
        """
        process_form_callback: called when the form is filled.
        """
        self.fields = fields
        self.cur_field_no = 0
        self.process_form_callback = process_form_callback
        self.destructor_callback = None
        self.user_id = None

    def get_cur_field(self) -> Field:
        if not self.cur_field_no_outofrange():
            return self.fields[self.cur_field_no]
        raise IndexError("form.get_cur_field: `cur_field_no` out of range.")

    def _set_field_value(self, field: Field, value: Any):
        """
        Mostly ensures the values set to the fields are of appropriate types.
        """
        if not isinstance(value, field.built_in_type):
            raise TypeError(
                f"form.set_field_value: `{field.title}` must be a `{field.built_in_type}`."
            )
        field.value = value

    def fill(self, field: Field, upd: dict) -> bool:
        if not field.check_update_validity(upd):
            server.send_message(
                f"You should provide a {field.descriptive_type}.",
                chat_id=upd["chat_id"],
            )
            return False
        field_value = field.parse_from_update(upd)
        self._set_field_value(field, field_value)
        return True

    def switch_next_field(self):
        self.cur_field_no += 1
        if self.cur_field_no_outofrange():
            self.cur_field_no -= 1
            raise IndexError("form.switch_next_field: No more fields.")

    def process(self, user_id: int, chat_id: int):
        self.process_form_callback(self, user_id, chat_id)

    def is_finished(self) -> bool:
        for field in self.fields:
            if field.value is None:
                return False
        return True

    def prompt_field(self, field: Field, chat_id: int):
        server.send_message(text=field.prompt, chat_id=chat_id)

    def end(self):
        if self.destructor_callback is not None:
            self.destructor_callback(self)
        else:
            raise RuntimeError("form.end: Destructor callback hasn't been set.")

    def serialize_fields_to_dict(self) -> Dict:
        return {field.title: field.value for field in self.fields}

    def cur_field_no_outofrange(self):
        return self.cur_field_no < 0 or self.cur_field_no >= len(self.fields)

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def set_destructor(self, destructor_callback: Callable):
        self.destructor_callback = destructor_callback
