"""A module to manage user's data stored locally"""

import os
import sqlite3
from typing import List, Dict

import server


class _DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv("DATABASE_URI"))
        self.cursor = self.conn.cursor()

    def add(self, table: str, fields: Dict) -> int:
        """
        Inserts a row (fields dictionary) into the table.

        Returns:
            The ID of the added row.
        """
        # Parse keys and values to compose an SQL query.
        keys = ', '.join(fields.keys())
        values = tuple(fields.values())
        self.cursor.execute(
            f"""INSERT INTO {table} ({keys})
                             VALUES({', '.join(['?']*len(values))})""",
            values,
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def delete(self, table: str, id: int):
        """Deletes the row with the specified ID."""
        self.cursor.execute(f"""DELETE FROM {table} WHERE id = ?""", (id,))
        self.conn.commit()

    def modify(self, table: str, changes: Dict, **filter_):
        """
        Changes the row with the specified ID.

        Args:
            changes: A {field_name: field_value} dictionary. Doesn't have to contain all columns.
            filter_: An argument-value pair (e.g., user_id=`id`).
        """
        sql_command = f"""UPDATE {table} SET """
        last_field_name = list(changes.keys())[-1]
        for field_name, value in changes.items():
            sql_command += f"{field_name} = {value} "
            if field_name != last_field_name:
                sql_command += ", "
        sql_command += f"WHERE {filter_.keys()[0]} = {filter_.values()[0]}"
        self.cursor.execute(sql_command)
        self.conn.commit()

    def filter_(self, table: str, filters: Dict) -> List:
        """Returns a list of all rows with specified filters met."""
        sql_command = f"""SELECT * FROM {table} WHERE """
        last_field_name = list(filters.keys())[-1]
        for field_name, value in filters.items():
            sql_command += f"{field_name} LIKE '%{value}%'"
            if field_name != last_field_name:
                sql_command += " AND "
        self.cursor.execute(sql_command)
        return [
            self.parse_sql_response_to_dict(table, row_values)
            for row_values in self.cursor.fetchall()
        ]

    def get(self, table: str, params: Dict) -> dict:
        """Returns a single row with specified row values (usually, id is used because it's unique to every database entry)."""
        sql_command = f"""SELECT * FROM {table} WHERE """
        last_field_name = list(params.keys())[-1]
        for field_name, value in params.items():
            sql_command += f"{field_name} = '{value}'"
            if field_name != last_field_name:
                sql_command += " AND "
        self.cursor.execute(sql_command)
        row = self.cursor.fetchone()
        if row is not None:
            return self.parse_sql_response_to_dict(table, row)
        else:
            return None

    def parse_sql_response_to_dict(self, table: str, values: List) -> Dict:
        """Takes an SQL response as a list of a row's values and returns a dictionary with list values' field names specified."""
        # Returns a list of table's column names.
        self.cursor.execute(f"""SELECT name FROM PRAGMA_TABLE_INFO('{table}')""")
        field_names = [i[0] for i in self.cursor.fetchall()]
        return dict(zip(field_names, values))


_db = _DataBase()


def shutdown():
    """Will be called when the program is stopped."""
    _db.conn.close()


class _DataBaseTable:
    table_name: str

    @classmethod
    def add(cls, fields: Dict) -> int:
        """Returns the ID of the added row."""
        return _db.add(table=cls.table_name, fields=fields)

    @classmethod
    def delete(cls, /, *, id: int):
        _db.delete(table=cls.table_name, id=id)

    @classmethod
    def modify(cls, changes: Dict, /, *, filter_):
        _db.modify(table=cls.table_name, changes=changes, filter_=filter_)

    @classmethod
    def get(cls, params: Dict) -> Dict:
        return _db.get(table=cls.table_name, params=params)

    @classmethod
    def filter_(cls, filters: Dict) -> List:
        return _db.filter_(table=cls.table_name, filters=filters)


class Product(_DataBaseTable):
    table_name = "products"

    @staticmethod
    def send_to_user(
        product: Dict, chat_id: int, send_product_id: bool = False
    ) -> Dict:
        """
        Sends a product as a photo with a caption to the specified chat.

        Args:
            send_product_id: If set True, product['id'] will be sent as well.
        """
        seller_chat_id = User.get({"tg_user_id": product["seller_tg_id"]})["tg_chat_id"]
        product["seller"] = f"@{server.get_chat(seller_chat_id)['username']}"
        del product["seller_tg_id"]
        if not send_product_id:
            del product["id"]
        photo_caption = "<b>"
        for field, val in product.items():
            if isinstance(val, str) or isinstance(val, int):
                if field == "id":
                    field = field.upper()
                else:
                    field = field.capitalize()
                photo_caption += f"<i>{field}</i>:  {val}\n"
        photo_caption += "</b>"
        return server.send_photo(
            photo=product["photo"],
            chat_id=chat_id,
            caption=photo_caption,
            parse_mode="html",
        )


class User(_DataBaseTable):
    table_name = "users"

    @classmethod
    def is_registered(cls, id: int) -> bool:
        # classmethod is used since table_name is required
        # in order to access the database.
        return super(User, cls).get({"tg_user_id": id}) is not None


class Region(_DataBaseTable):
    table_name = "regions"

    @classmethod
    def get(cls, params: Dict) -> Dict:
        """
        If region has already been added to the database, returns it.
        Otherwise, creates a new database entry.
        """
        if (region := super(Region, cls).get(params)) is not None:
            return region
        else:
            region_id = super(Region, cls).add(params)
            return super(Region, cls).get({"id": region_id})
        