from forms.field_types import FieldType
from forms.field import Field
from forms.form import Form
from forms.form_processing import *  # functions to process form_templates.

# * FIELD_NAME: (FIELD_TYPE, FIELD_PROMPT)


NEW_PRODUCT_FORM = Form(
    fields=[
        Field("name", FieldType.STRING, "Type a product name."),
        Field(
            "description", FieldType.STRING, "Send me a description of your product."
        ),
        Field("photo", FieldType.PHOTO, "Send me a photo."),
        Field(
            "price", FieldType.NATURAL_NUM, "How much will the product cost (in USD)?"
        ),
    ],
    process_form_callback=process_new_product_form,
)


DELETE_PRODUCT_FORM = Form(
    fields=[
        Field(
            "product_id",
            FieldType.NATURAL_NUM,
            "Send me the ID of the product you want to delete.",
        )
    ],
    process_form_callback=process_delete_product_form,
)


NEW_USER_FORM = Form(
    fields=[
        Field(
            "location",
            FieldType.LOCATION,
            ("Send me your location, please. I need it to match sellers "
             "with buyers based on where they live."),
        )
    ],
    process_form_callback=process_new_user_form,
)


NEW_USER_LOCATION_FORM = Form(
    fields=[Field("location", FieldType.LOCATION, "Send me your new location.")],
    process_form_callback=process_new_user_location_form,
)


SEARCH_QUERY_FORM = Form(
    fields=[Field("query", FieldType.STRING, "Send me a query.")],
    process_form_callback=process_search_query_form,
)

__all__ = [
    "NEW_USER_FORM",
    "NEW_PRODUCT_FORM",
    "DELETE_PRODUCT_FORM",
    "NEW_USER_LOCATION_FORM",
    "SEARCH_QUERY_FORM",
]
