import sqlite3

# TODO:  no need to user this file after using sqlalchemy ORM


# Uniform Resource Identifier URI
connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY , username text, password text)"

create_item_table = "CREATE TABLE IF NOT EXISTS items (item_id INTEGER PRIMARY KEY , item_name text, price real)"
cursor.execute(create_user_table)
cursor.execute(create_item_table)

# cursor.execute("INSERT INTO items VALUES (NUll, 'nova3i', '12.5')")
# cursor.execute("INSERT INTO items VALUES (NUll, 'hp', '15.00')")
# cursor.execute("INSERT INTO items VALUES (NUll, 'macpro', '109.523')")
connection.commit()
connection.close()
