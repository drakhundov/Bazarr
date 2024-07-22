import os
import sys

import bot
import commands
import forms
import server


def handle_update(upd: dict):
    """Receives and responds to updates from the Telegram Bot API."""
    # There will always be a user_id and a chat_id.
    user_id = upd["user_id"]
    chat_id = upd["chat_id"]
    # If update is a new command (a new message from a user) to be executed.
    if upd.get("message") and upd["message"].startswith("/"):
        # Get rid of the '/'.
        command = upd["message"][1:]
        commands.execute_command(command, upd=upd)
    else:
        # If there is an ongoing form.
        if (form := forms.get(user_id)) is not None:
            success = form.fill(form.get_cur_field(), upd)
            if form.is_finished():
                form.process(user_id, chat_id)
                form.end()
            elif success:
                form.switch_next_field()
                form.prompt_field(form.get_cur_field(), chat_id)
        else:
            commands.exec_help_cmd(upd)


if "--clear" in sys.argv:
    server.get_updates(offset=-1)

env_vars = ["TOKEN", "API_URL", "GETFILE_API_URL", "DATABASE_URI"]
for env_var in env_vars:
    if os.getenv(env_var) is None:
        raise RuntimeError(
            "Environment variables were not defined. Use `source initenv.sh`."
        )

bot.run(handle_update)
