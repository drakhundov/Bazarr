# Bazarr
## **A Telegram bot to buy and sell products.**
### Video Demo:  https://www.youtube.com/watch?v=R2PsWDDurlo

## User Commands
### - ```/start``` - *start the bot and register if not registered yet*
### - ```/new``` - *add a new product*
### - ```/delete``` - *delete a product (the bot will send all products with corresponding IDs and ask for the ID of the product to be deleted)*
### - ```/myproducts``` - *list all products added*
### - ```/search``` - *search for a product (will be prompted to type a query)*
### - ```/newlocation``` - *send the bot your new location (locations are used to offer users products nearby)*

### I used [*Telegram Bot API*](https://core.telegram.org/bots/api) and its methods:
- [getUpdates](https://core.telegram.org/bots/api#getupdates)
- [sendMessage](https://core.telegram.org/bots/api#sendmessage)
- [sendPhoto](https://core.telegram.org/bots/api#sendphoto)
- [getFile](https://core.telegram.org/bots/api#getfile)
- [getChat](https://core.telegram.org/bots/api#getchat)

### Modules:

> [***server.py***](server.py)

Deals with the Telegram Bot API server. It's used to get users' messages and send information to users. It contains *access* as the main function and a separate function for each of the Telegram Bot API methods used.

> [***bot.py***](bot.py)

Receives, parses, and processes updates. Contains only two functions:
- ```run(handle_update)``` to actually run the bot
- ```_parse_update(upd)``` to take the most important information out of an update

> [***main.py***](main.py)

Can be used to run the bot via ```python main.py```

Contains only two functions:
- ```handle_update(upd)``` receives updates from the *bot.py* and deals with them
- ```execute(command, upd)``` runs user commands (e.g. ```execute('new', upd=upd)```)

> [**data.py**](data.py)

Deals with the data stored locally.
You can check the schema [here](schema.sql).

The [*database*](data.db) contains the following tables:
- **users** (tg_user_id, tg_chat_id, area_id)  *a list of all users with their locations stored in area_id*
- **regions** (id, ISO name (e.g. TR34))  *every time a user sends a location, it will be searched in the database; if there's no such location, it will be added to this table*
- **products** (id, name, description, photo, price, seller_tg_id) *a list of all products currently on sale*

There's a separate class for each table denoted as a table's name singular and capitalized (products -> class Product). These classes can be used to modify the database. There are several main methods the classes contain:
- ```add(**fields)``` to add an entry into the database
- ```delete(id)``` to delete the row with specified ID
- ```modify(changes, id)``` to change the row with specified ID; takes a dictionary (positional only) and an ID (keyword only)
- ```get(**params)``` to obtain a particular row; returns a single row that meets 'params'
- ```filter_(**filters)``` to find rows with column values specified; returns all rows that meet the filters

> [**geo.py**](geo.py)

Used only to get an address by passing latitude and longitude to the ```geo.get()``` function.

> [**forms.py**](forms.py)

Used to create forms (basically, fields of data user is required to fill by sending messages to the bot). Forms that can be used are stored as constants:
- **NEW_PRODUCT**
- **DELETE_PRODUCT**
- **NEW_USER**
- **NEW_USER_LOCATION**
- **SEARCH_QUERY**

There is a class called ```_Form```, which requires every field passed as a keyword argument with its name and a tuple that contains the field's abstract type (```STRING, NATURAL_NUM, PHOTO, LOCATION```) and the prompt that should be sent to the user (e.g. ```_Form(field_name=(_Field.STRING, 'type a string.'))```).

The following functions are used to deal with forms:
- ```get(user_id)``` returns the current form for the user specified
- ```start(user_id, form)```, where form is one of the constants above
- ```end(user_id)```
- ```fill(upd)```, where upd is an update
- ```request_next_field(user_id, chat_id)``` sends a prompt to the user's chat
