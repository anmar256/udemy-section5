import sqlite3

connection = sqlite3.connect('data.db')

curser = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
curser.execute(create_table)

user1 = (1, 'anmar256', '214365')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
curser.execute(insert_query, user1)

users = [
    (2, 'Rolf', '123456'),
    (3, 'Ali', 'asdf'),
    (4, 'Reza', 'boz'),
]
curser.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in curser.execute(select_query):
    print(row)
connection.commit()

connection.close()