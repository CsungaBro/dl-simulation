from mysql.connector import connect, Error
import logging


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
            logging.info(f"Database: {self.database_name} created")
        except Error as e:
            logging.error(e)
            logging.error(f"Databse: {self.database_name} creation failed")

    def create_table(self):
        create_table_command = f"""        
        CREATE TABLE {self.table_name}(
            sim_id int AUTO_INCREMENT PRIMARY KEY, 
            hash_id VARCHAR(50),
            c DECIMAL(3,3), 
            d DECIMAL(3,3), 
            h DECIMAL(3,3), 
            r DECIMAL(3,3),
            generated INT,
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
            logging.info(f"Table: {self.table_name} created")
        except Error as e:
            logging.error(e)
            logging.error(f"Table: {self.table_name} creation failed")


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
            logging.error(e)      

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
                        logging.info(row)
        except Error as e:
            logging.error(e)

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
                    logging.debug(cursor)
                    for x in cursor:
                        logging.debug(x[0])
                        is_it_in = True
            return is_it_in
        except Error as e:
            logging.error(e)   

    def data_adder(self, hash_data, c, d, h, r):
        command = f"""
            INSERT INTO {self.table_name}
            (hash_id, c, d, h, r) 
            VALUES (%s, %s, %s, %s, %s)
        """
        logging.debug(command)
        insert_values = (hash_data, float(c), float(d), float(h), float(r))
        logging.debug(insert_values)
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
            logging.info(f"{hash_data} added")
        except Error as e:
            logging.error(f"{hash_data} NOT added")
            logging.error(e) 
  
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
                    logging.debug(cursor)
                    for x in cursor:
                        logging.debug(x[0])
                        sim_name = f"sim_{x[0]}_{hash_data}"
        except Error as e:
            logging.error(e)   
        return sim_name
    
    def data_setter_handler(self, c, d, h, r):
        hash_data = self.hash_data_maker(c, d, h, r)
        if not self.already_added_checker(hash_data):
            self.data_adder(hash_data, c, d, h, r)
        else:
            logging.error("It's already in the database")

    def data_getter_handler(self, c, d, h, r):
        hash_data = self.hash_data_maker(c, d, h, r)
        logging.info(f"data_getter_handler:{hash_data}")
        # Here is the problem
        sim_name = self.sim_name_maker(hash_data)
        logging.info(f"data_getter_handler:{sim_name}")
        return sim_name