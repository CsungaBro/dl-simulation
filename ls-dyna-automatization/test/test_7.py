import mysql.connector
from datetime import datetime 

db = mysql.connector.connect(
    host="localhost",
    user="csunga",
    passwd="root",
    database="testdatabase"
)

my_cursor = db.cursor()

# my_cursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
# my_cursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("TIM", datetime.now(), 'M'))
# my_cursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("JOE", datetime.now(), 'M'))
# my_cursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s, %s, %s)", ("VIKI", datetime.now(), 'F'))
# db.commit()

# my_cursor.execute("SELECT name, id FROM Test WHERE gender = 'M' ORDER BY id DESC")

# my_cursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")

my_cursor.execute("ALTER TABLE Test CHANGE first_name first_name VARCHAR(4)")

my_cursor.execute("DESCRIBE Test")

for x in my_cursor:
    print(x)
    # y = x[1]+10
    # print(y)