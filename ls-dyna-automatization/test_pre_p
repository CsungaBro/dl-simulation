import pandas as pd
import numpy as np
import os
from logger import csu_logger as csu_logger
from abc import ABC, abstractclassmethod
import regex as re
from mysql.connector import connect, Error


class DataBaseHandler(ABC):
    def __init__(self, database_dir) -> None:
        self.database_dir = database_dir

    def read_database(self) -> None:
        database_exist = os.path.exists(self.database_dir)
        if not database_exist:
            logger.info("No Database Found")
            self._data_base_maker()
        else:
            logger.info(f"{self.database_dir} found")
            self.data = pd.read_csv(self.database_dir)
        logger.info(self.data)

    def _data_base_maker(self) -> None:
        columns = ["Hash_ID","name","c","d","h","r"]
        c = 120
        d = 120
        h = 27.75
        r = 6.5
        hash_id = self.id_hash_maker(c, d, h, r)
        name = self.name_generator(hash_id, 0)
        first_column = [hash_id, name, c, d, h, r]
        self.data = pd.DataFrame(np.array([first_column]), columns=columns)

    def write_database(self):
        numb = re.findall("[0-9]+", self.database_dir)[0]
        numb = int(numb)
        numb += 1 
        self.new_database_path = re.sub("[0-9]+", f"{numb}", self.database_dir)
        logger.info(self.new_database_path)
        self.data.to_csv(self.database_dir)

    def id_hash_maker(self, c, d, h, r,) -> str:
        return f"{c}x{d}x{h}_R{r}"
    
    def name_generator(self, hash_id, sim_number) -> str:
        return f"sim_{sim_number}_{hash_id}"
    
    def check_if_new(self, new_hash_id):
        is_it_in = self.data.isin([new_hash_id])

    def data_adder(self, c, d, h, r):
        new_hash_id = self.id_hash_maker(c, d, h, r)
        if self.check_if_new(new_hash_id):
            sim_number = self.data.iloc[-1][0]
            logger.debug(sim_number)

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

def main():
    logger.info("main")
    db_name = "Test_Paramaters"
    table_name = "Test_parameters"
    DBE = DataBaseExecutor(db_name, table_name)
    DC = DataCreator()
    create_db_command = """
    CREATE TABLE Test_parameters(
        sim_id int AUTO_INCREMENT PRIMARY KEY, 
        hash_id VARCHAR(50),
        c DECIMAL(3,3), 
        d DECIMAL(3,3), 
        h DECIMAL(3,3), 
        r DECIMAL(3,3),
        UNIQUE(hash_id)
    )
    """
    # for db_parameter in ["c","d","h","r"]:
    #     alter_command = f"""
    #         ALTER TABLE {table_name}
    #         MODIFY COLUMN {db_parameter} DECIMAL(10,3)
        
    #     """
    #     DBE.execute_command(alter_command)
    # DBE.create_database(db_name)
    # DBE.create_table(create_db_command, table_name)
    DBE.describe_table()
    c, d, h, r = 120, 120, 27.5, 6.5
    hash_id = DC.hash_creator(c, d, h, r)
    DBE.new_data_adder(hash_id, c, d, h, r)
    c, d, h, r = 120, 120, 33.75, 6.5
    hash_id = DC.hash_creator(c, d, h, r)
    DBE.new_data_adder(hash_id, c, d, h, r)
    c, d, h, r = 120, 120, 33.75, 11.0
    hash_id = DC.hash_creator(c, d, h, r)
    DBE.new_data_adder(hash_id, c, d, h, r)        
    # DBH.data_adder(120, 120, 33.75, 6.5)
    # DBH.write_database()


if __name__ == "__main__":
    logger = csu_logger.logger_init()
    main()