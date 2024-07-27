from typing import Dict

import data
import forms
import server


def exec_register_cmd(upd: Dict):
    form = forms.start(upd["user_id"], forms.NEW_USER_FORM)
    form.prompt_field(form.get_cur_field(), upd["chat_id"])


def exec_start_cmd(upd: Dict):
    server.send_message(
        text=f'<b> Hi, @{upd["username"]}! How can I help you? </b>',
        chat_id=upd["chat_id"],
        parse_mode="html",
    )
    if not data.User.is_registered(upd["user_id"]):
        exec_register_cmd(upd)


def exec_new_cmd(upd: Dict):
    if not data.User.is_registered(upd["user_id"]):
        server.send_message("You must register first.", chat_id=upd["chat_id"])
        exec_register_cmd(upd)
        return
    form = forms.start(upd["user_id"], forms.NEW_PRODUCT_FORM)
    form.prompt_field(form.get_cur_field(), upd["chat_id"])


def exec_delete_cmd(upd: Dict):
    for product in data.Product.filter_({"seller_tg_id": upd["user_id"]}):
        data.Product.send_to_user(product, upd["chat_id"], send_product_id=True)
    form = forms.start(upd["user_id"], forms.DELETE_PRODUCT_FORM)
    form.prompt_field(form.get_cur_field(), upd["chat_id"])


def exec_search_cmd(upd: Dict):
    form = forms.start(upd["user_id"], forms.SEARCH_QUERY_FORM)
    form.prompt_field(form.get_cur_field(), upd["chat_id"])


def exec_myproducts_cmd(upd: Dict):
    products_found = data.Product.filter_({"seller_tg_id": upd["user_id"]})
    if not products_found:
        server.send_message(
            text="You don't have any products yet. To add a product type <i> /new </i>",
            chat_id=upd["chat_id"],
            parse_mode="html",
        )
    for product in products_found:
        data.Product.send_to_user(product, upd["chat_id"])


def exec_newlocation_cmd(upd: Dict):
    form = forms.start(upd["user_id"], forms.NEW_USER_LOCATION_FORM)
    form.prompt_field(form.get_cur_field(), upd["chat_id"])


def exec_help_cmd(upd: Dict):
    server.send_message(
        text=(
            "<b>/start</b> - start the bot\n"
            "<b>/new</b> - add a new product\n"
            "<b>/delete</b> - delete a product\n"
            "<b>/search</b> - search for products\n"
            "<b>/myproducts</b> - list all products on sale\n"
            "<b>/newlocation</b> - change location\n"
        ),
        chat_id=upd["chat_id"],
        parse_mode="html",
    )


COMMANDS_MAP = {
    "start": exec_start_cmd,
    "new": exec_new_cmd,
    "delete": exec_delete_cmd,
    "search": exec_search_cmd,
    "myproducts": exec_myproducts_cmd,
    "newlocation": exec_newlocation_cmd,
    "help": exec_help_cmd,
    "register": exec_register_cmd,
}


def execute_command(command: str, /, *, upd: dict):
    """Executes the command specified."""
    if (executioner := COMMANDS_MAP.get(command)) is None:
        server.send_message(text=f"Invalid command: {command}.", chat_id=upd["chat_id"])
        return
    executioner(upd)
