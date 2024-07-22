import data
import forms
import geo
import server
from forms.form import Form


def process_new_product_form(form: Form, user_id: int, chat_id: int):
    fields_dict = form.serialize_fields_to_dict()
    fields_dict["seller_tg_id"] = user_id
    data.Product.add(fields_dict)
    server.send_message(text="Your product have been saved.", chat_id=chat_id)


# TODO Restore products after deleting (add a deleted column to the db and if user deletes a product, set it to True)
def process_delete_product_form(form: Form, user_id: int, chat_id: int):
    fields_dict = form.serialize_fields_to_dict()
    product_id = fields_dict["product_id"]
    data.Product.delete(id=product_id)
    server.send_message(
        text=f"The product <i> #{product_id} </i> has been deleted.",
        chat_id=chat_id,
        parse_mode="html",
    )


def process_new_user_form(form: Form, user_id: int, chat_id: int):
    fields_dict = form.serialize_fields_to_dict()
    region_name = geo.get(*fields_dict["location"])
    region = data.Region.get({"name": region_name})
    data.User.add(
        {"tg_user_id": user_id, "tg_chat_id": chat_id, "region_id": region["id"]}
    )
    server.send_message(text="You've been successfully registered.", chat_id=chat_id)


def process_new_user_location_form(form: Form, user_id: int, chat_id: int):
    fields_dict = form.serialize_fields_to_dict()
    region_name = geo.get(*fields_dict["location"])
    region = data.Region.get({"name": region_name})
    data.User.modify({"region_id": region["id"]}, tg_user_id=user_id)
    server.send_message(text="The new location has been saved.", chat_id=chat_id)


def process_search_query_form(form: Form, user_id: int, chat_id: int):
    fields_dict = form.serialize_fields_to_dict()
    products_found = data.Product.filter_(
        {"name": fields_dict["query"], "description": fields_dict["query"]}
    )
    user_region_id = data.User.get({"tg_user_id": user_id})["region_id"]
    if len(products_found) == 0:
        server.send_message(
            "Nothing found for the given query. Try something else.", chat_id=chat_id
        )
        # TODO: implement argument passing to forms
        # TODO: so that it doesnt ask for a query next time.
        forms.start(user_id, forms.SEARCH_QUERY_FORM)
    for product in products_found:
        seller_id = None
        seller_region_id = None
        if (
            seller := data.User.get({"tg_user_id": product["seller_tg_id"]})
        ) is not None:
            seller_id = seller["tg_user_id"]
            seller_region_id = seller["region_id"]
            if seller_region_id is None:
                continue
        # If seller and buyer live in the same area.
        if seller_region_id == user_region_id and seller_id != user_id:
            data.Product.send_to_user(product, chat_id)
