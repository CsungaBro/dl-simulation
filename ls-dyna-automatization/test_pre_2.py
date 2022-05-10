from mysql.connector import connect, Error
from abc import ABC, abstractclassmethod
from logger import csu_logger as csu_logger


class DataBaseExecutor(ABC):
    def __init__(self, database_name, table_name) -> None:
        self.database_name = database_name
        self.table_name = table_name
    
    def create_database(self, database_name):
        command = f"CREATE DATABASE {database_name}"
        try:    
            with connect(
                host="localhost",
                user="csunga",
                password="root"
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    connection.commit()
            self.database_name = database_name
            logger.info(f"Database: {self.database_name} created")
        except Error as e:
            logger.error(e)
            logger.error(f"Databse: {database_name} creation failed")

    def create_table(self, command, table_name):
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    connection.commit()
            self.table_name = table_name
            logger.info(f"Table: {self.table_name} created")
        except Error as e:
            logger.error(e)
            logger.error(f"Table: {table_name} creation failed")

    def execute_command(self, command):
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
        except Error as e:
            logger.error(e)        

    def describe_table(self):
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"DESCRIBE {self.table_name}")
                    for row in cursor:
                        logger.info(row)
        except Error as e:
            logger.error(e)
    
    def hash_checker(self, hash_id):
        command = f"SELECT hash_id FROM {self.table_name}"
        is_it_new = None
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    for db_hash_id in cursor:
                        logger.debug(f"db_hash_id: {db_hash_id} new hasd_id: {hash_id}")
                    if hash_id in cursor:
                        is_it_new = False
                    else:
                        is_it_new = True
        except Error as e:
            logger.error(e)             
        return is_it_new

    def data_adder(self, hash_id, c, d, h, r):
        command = f"""
            INSERT INTO {self.table_name}
            (hash_id, c, d, h, r) 
            VALUES (%s, %s, %s, %s, %s)
        """
        logger.debug(command)
        insert_values = (hash_id, float(c), float(d), float(h), float(r))
        logger.debug(insert_values)
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command, insert_values)
                    connection.commit()
            logger.info(f"{hash_id} added")
        except Error as e:
            logger.error(f"{hash_id} NOT added")
            logger.error(e) 
    
    def new_data_adder(self, hash_id, c, d, h, r):
        if self.hash_checker(hash_id):
            self.data_adder(hash_id, c, d, h, r)

class DataCreator(ABC):
    def hash_creator(self, c, d, h, r):
        return f"{c}x{d}x{h}_R{r}"


class MySQLHandler:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

    def create_database(self):
        
        command = f"CREATE DATABASE {self.database_name}"
        try:    
            with connect(
                host="localhost",
                user="csunga",
                password="root"
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
                    connection.commit()
            logger.info(f"Database: {self.database_name} created")
        except Error as e:
            logger.error(e)
            logger.error(f"Databse: {self.database_name} creation failed")

    def create_table(self):
        create_table_command = f"""        
        CREATE TABLE {self.table_name}(
            sim_id int AUTO_INCREMENT PRIMARY KEY, 
            hash_id VARCHAR(50),
            c DECIMAL(3,3), 
            d DECIMAL(3,3), 
            h DECIMAL(3,3), 
            r DECIMAL(3,3),
            UNIQUE(hash_id)
        )
        """        
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_table_command)
                    connection.commit()
            logger.info(f"Table: {self.table_name} created")
        except Error as e:
            logger.error(e)
            logger.error(f"Table: {self.table_name} creation failed")


    def command_executor(self, command):
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command)
        except Error as e:
            logger.error(e)      

    def describe_table(self):
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"DESCRIBE {self.table_name}")
                    for row in cursor:
                        logger.info(row)
        except Error as e:
            logger.error(e)

    def already_added_checker(self, hash_data):
        is_it_in = False
        command = f'''
        SELECT sim_id 
        FROM {self.table_name}
        WHERE hash_id = "{hash_data}" 
        '''
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(command)
                    logger.debug(cursor)
                    for x in cursor:
                        logger.debug(x[0])
                        is_it_in = True
            return is_it_in
        except Error as e:
            logger.error(e)   

    def data_adder(self, hash_data, c, d, h, r):
        command = f"""
            INSERT INTO {self.table_name}
            (hash_id, c, d, h, r) 
            VALUES (%s, %s, %s, %s, %s)
        """
        logger.debug(command)
        insert_values = (hash_data, float(c), float(d), float(h), float(r))
        logger.debug(insert_values)
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(command, insert_values)
                    connection.commit()
            logger.info(f"{hash_data} added")
        except Error as e:
            logger.error(f"{hash_data} NOT added")
            logger.error(e) 
  
    def hash_data_maker(self, c, d, h, r):
        return f"{c}x{d}x{h}_R{r}"

    def sim_name_maker(self, hash_data):
        command = f'''
        SELECT sim_id 
        FROM {self.table_name}
        WHERE hash_id = "{hash_data}" 
        '''
        sim_name = ""
        try:
            with connect(
                host="localhost",
                user="csunga",
                password="root",
                database=self.database_name
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(command)
                    logger.debug(cursor)
                    for x in cursor:
                        logger.debug(x[0])
                        sim_name = f"sim_{x[0]}_{hash_data}"
        except Error as e:
            logger.error(e)   
        return sim_name
    
    def data_setter_handler(self, c, d, h, r):
        hash_data = self.hash_data_maker(c, d, h, r)
        if not self.already_added_checker(hash_data):
            self.data_adder(hash_data, c, d, h, r)
        else:
            logger.error("It's already in the database")

    def data_getter_handler(self, c, d, h, r):
        hash_data = self.hash_data_maker(c, d, h, r)
        sim_name = self.sim_name_maker(hash_data)
        return sim_name, c, d, h, r

def main(c, d, h, r):    

    db_name = "Test_Paramaters"
    table_name = "test_parameters"

    sql_handler = MySQLHandler(db_name, table_name)

    sql_handler.data_base_maker()
    sql_handler.table_maker()
    
    sql_handler.data_setter_handler(c, d, h, r)
    names = sql_handler.data_getter_handler(c, d, h, r)
    logger.info(names)

if __name__ == "__main__":
    logger = csu_logger.logger_init()
    c, d, h, r = 120, 120, 27.5, 6.1
    main(c, d, h, r)