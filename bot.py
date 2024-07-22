import sys
import time

import data
import server


def run(handle_update: callable):
    """
    Runs the bot and deals with updates. Stops on keyboard interruption.

    Args:
        handle_update: A function to be run with every new update passed to it.
    """
    last_update_id = -1
    print("Listening.")
    while True:
        try:
            updates = server.get_updates(offset=last_update_id + 1)
            for update in updates:
                if (update := _parse_update(update)) is not None:
                    handle_update(update)
            if updates:
                last_update_id = updates[-1]["update_id"]
        except KeyboardInterrupt:
            data.shutdown()
            sys.exit(0)
        finally:
            time.sleep(0.01)


def _parse_update(upd: dict) -> dict:
    """
    Receives a Telegram Bot API update as a dictionary and
    returns the most important data out of it.
    """
    if upd.get("message") is None:
        return None
    parsed_upd = {
        "user_id": upd["message"]["from"]["id"],
        "username": upd["message"]["from"]["username"],
        "chat_id": upd["message"]["chat"]["id"],
    }
    if upd["message"].get("text"):
        parsed_upd["message"] = upd["message"]["text"]
    elif upd["message"].get("document"):
        parsed_upd["file_id"] = upd["message"]["document"]["file_id"]
    elif upd["message"].get("location"):
        parsed_upd["longitude"] = upd["message"]["location"]["longitude"]
        parsed_upd["latitude"] = upd["message"]["location"]["latitude"]
    elif upd["message"].get("photo"):
        parsed_upd["photo"] = upd["message"]["photo"]
        parsed_upd["file_id"] = upd["message"]["photo"][-1]["file_id"]
    return parsed_upd
