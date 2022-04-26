from dataclasses import dataclass
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="testdatabase"
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE testdatabase")
# my_cursor.execute("CREATE TABLE Parameters (hash_ID VARCHAR(50), name VARCHAR(50), c DECIMAL(3,3), d DECIMAL(3,3), h DECIMAL(3,3), r DECIMAL(3,3))")
# my_cursor.execute("DESCRIBE Parameters")
def insert_into_test(c, d, h, r):
  new_hash_id = id_hash_maker(c, d, h, r)
  sim_name = name_generator(new_hash_id, 0)
  sql_insert_str = f"INSERT INTO Parameters (hash_ID, name, c, d, h, r) VALUES ({new_hash_id},{sim_name},{c},{d},{h},{r})"
  print(sql_insert_str)
  new_cursor = mydb.cursor()
  new_cursor.execute(sql_insert_str)

def name_generator(hash_id, sim_number) -> str:
    return f"sim_{sim_number}_{hash_id}"  

def id_hash_maker(c, d, h, r,) -> str:
    return f"{c}x{d}x{h}_R{r}"

insert_into_test(120, 120, 27.5, 6.5)
mydb.commit()
insert_into_test(120, 120, 33.75, 6.5)    
mydb.commit()
my_cursor.execute("SELECT * FROM Parameters")

for x in my_cursor:
  print(x)