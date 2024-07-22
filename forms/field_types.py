from forms.field_handler import FieldHandler


class FieldType:
    STRING = {
        "descriptive_type": "string",
        "built_in_type": str,
        "check_from_update_func": FieldHandler.check_string_from_update,
        "get_from_update_func": FieldHandler.get_string_from_update,
    }
    NATURAL_NUM = {
        "descriptive_type": "natural number",
        "built_in_type": int,
        "check_from_update_func": FieldHandler.check_natural_num_from_update,
        "get_from_update_func": FieldHandler.get_natural_num_from_update,
    }
    PHOTO = {
        "descriptive_type": "photo",
        "built_in_type": bytes,
        "check_from_update_func": FieldHandler.check_photo_from_update,
        "get_from_update_func": FieldHandler.get_photo_from_update,
    }
    LOCATION = {
        "descriptive_type": "location",
        "built_in_type": tuple,
        "check_from_update_func": FieldHandler.check_location_from_update,
        "get_from_update_func": FieldHandler.get_location_from_update,
    }
