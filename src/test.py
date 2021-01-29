import sqlite3

# Uniform Resource Identifier URI
connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = (
    "CREATE TABLE IF NOT EXISTS users (id int , username text, password text)"
)
cursor.execute(create_table)

user = (1, "jose", "pass123")
users = [(2, "jose", "pass123"), (3, "john", "passtest"), (4, "loen", "testpass")]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

# cursor.execute(insert_query, user)
# cursor.executemany(insert_query, users)

select_users = "SELECT * FROM users"
rows = cursor.execute(select_users)

for row in rows:
    print(row)

connection.commit()

connection.close()
