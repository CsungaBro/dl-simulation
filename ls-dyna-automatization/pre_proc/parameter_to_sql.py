
from mysql.connector import connect, Error
import pandas as pd
import logging
 
database_name = 'Test_Paramaters'
table_name   = "New_parameters"

df   = pd.read_pickle('test.pkl')    

create_table_command = f"""        
CREATE TABLE {table_name}(
    sim_id int AUTO_INCREMENT PRIMARY KEY, 
    hash_id VARCHAR(50),
    c DECIMAL(3,3), 
    d DECIMAL(3,3), 
    h DECIMAL(3,3), 
    r DECIMAL(3,3),
    generated TINYINT,
    UNIQUE(hash_id)
)
"""      

print(create_table_command)

try:
    with connect(
        host="localhost",
        user="csunga",
        password="root",
        database=database_name
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table_command)
            connection.commit()
    logging.info(f"Table: {table_name} created")
except Error as e:
    logging.error(e)
    logging.error(f"Table: {table_name} creation failed")

try:
    with connect(
        host="localhost",
        user="csunga",
        password="root",
        database=database_name
    ) as connection:
        df.to_sql(table_name, connection, if_exists='fail')
    logging.info(f"Table: {table_name} created")
except Error as e:
    logging.error(e)
    logging.error(f"Table: {table_name} creation failed")



# sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1/test', pool_recycle=3600)
# dbConnection    = sqlEngine.connect()
# try:
#     frame           = dataFrame.to_sql(tableName, dbConnection, if_exists='fail');
# except ValueError as vx:
#     print(vx)
# except Exception as ex:   
#     print(ex)
# else:
#     print("Table %s created successfully."%tableName);   
# finally:
#     dbConnection.close()