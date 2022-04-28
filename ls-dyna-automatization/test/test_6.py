import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="csunga",
    passwd="root",
    database="testdatabase"
)

my_cursor = db.cursor()

# command_text = f"CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)"
# command_text = f"DESCRIBE Person"
# "INSERT INTO Person (name, age) VALUES ('tim', 15)"
p_name = 'tim'
p_age = 45
# command_text = f"INSERT INTO Person (name, age) VALUES ({p_name}, {p_age})"
# command_text = f"INSERT INTO Person (name, age) VALUES ('csenger', 25)"
# my_cursor.execute(command_text)
# db.commit()

read_text = "SELECT * FROM Person"
my_cursor.execute(read_text)

for x in my_cursor:
    print(x)