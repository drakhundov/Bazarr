import os

import requests

import caching

# Will be used to make requests to Telegram servers
# in order to receive updates and communicate with users.
API_URL = f"{os.getenv('API_URL')}{os.getenv('TOKEN')}"

# Will be used to download files from Telegram servers (if users send some).
GETFILE_URL = f"{os.getenv('GETFILE_API_URL')}{os.getenv('TOKEN')}"

# Standard HTTP methods (GET, POST) matched to
# Telegram Bot API methods that will be used.
HTTP_METHODS = {
    "GET": ("getUpdates", "getFile", "getChat",),
    "POST": ("sendMessage", "sendPhoto",)
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
}


def access(request: str, getfile: bool = False, files: dict = None, **args):
    """
    Transfers information to and gets information from Telegram Bot API.

    Args:
        request: Either one of the methods defined by Telegram to control the bot
                 (e.g. getUpdates, sendMessage) or a path to a file in the Telegram
                 Bot API servers.
        getfile: Whether request should be used as a path to a file (request is
                 supposed to be a Telegram Bot API method by default).
        args: Arguments (e.g. offset, message) passed to the server.
        files: Files should be specified separately as a dictionary,
               where files[file_name] should return the file's bytes.

    Returns:
        The server's response (a file, a list of updates, information about the
        message sent, etc.) if successful, an empty list if there are no updates.

    Raises:
        ValueError if method is invalid.
        FileNotFoundError if server couldn't find the specified document.
    """
    if getfile:
        url = f'{GETFILE_URL}/{request}'
        response = requests.get(url,headers=HEADERS, stream=True)
        if response.status_code != 200:
            # If not found (error 404).
            if response.status_code == 404:
                raise FileNotFoundError(
                    f'"server.access" can\'t locate the file "{request}"'
                )
            response.raise_for_status()
        file = bytes()
        for chunk in response.iter_content(chunk_size=8192):
            file += chunk
        return file
    # Query is a method.
    url = f'{API_URL}/{request}'
    if request in HTTP_METHODS['GET']:
        response = requests.get(url,headers=HEADERS, params=args)
    elif request in HTTP_METHODS['POST']:
        response = requests.post(url, data=args,headers=HEADERS, files=files)
    else:
        raise ValueError('Invalid method')
    data = response.json()
    if data['ok']:  # No error occurred.
        return data['result']
    response.raise_for_status()


def get_updates(offset: int = None, limit: int = 100) -> list:
    """
    Gets updates from the Telegram Bot API server (e.g. new messages from users).

    Args:
        offset: 'update_id' from which updates should be reported. All previous
                updates will be deleted. '-1' returns the last update.
        limit: Maximum number of updates to be returned.

    Returns:
        A list of recent updates.
    """
    return access('getUpdates', offset=offset, limit=limit)


def send_message(text: str, chat_id: int, parse_mode: str = None) -> dict:
    """
    Sends a message to a chat.

    Args:
        text: Message to be sent.
        chat_id: A unique identifier set to a chat by Telegram
                 (can be derived from an update).
        parse_mode: Specifies the way Telegram Bot API should read the message
                    (HTML, Markdown, MarkdownV2).
                    For example, text='<b> Bold text </b>' and parse_mode='HTML'
                    will render the 'text' using HTML.

    Returns:
        The server's response as a dictionary.
    """
    return access('sendMessage',
                  text=text,
                  chat_id=chat_id,
                  parse_mode=parse_mode)


def send_photo(photo: bytes, chat_id: int,
               caption: str = None, parse_mode: str = None) -> dict:
    return access('sendPhoto',
                  files={'photo': photo},
                  chat_id=chat_id,
                  caption=caption,
                  parse_mode=parse_mode)


def get_chat(chat_id: int) -> dict:
    """
    Obtains up-to-date information about the chat
    (e.g. a user's current username, user_id, etc.).
    """
    return access('getChat', chat_id=chat_id)


def get_file(file_id: int) -> str:
    """
    When user sends a file, a unique file_id will be given to the bot.
    Using the id, this function can get the file from Telegram Bot API.
    """
    file_path = access('getFile', file_id=file_id)['file_path']
    _bytes = access(file_path, getfile=True)
    caching.cache(caching.IMAGE, _bytes, _id=file_id)
    return file_id
