import pandas as pd
import numpy as np
import os
import logger.csu_logger as csu_logger
from abc import ABC, abstractclassmethod
import regex as re


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


def main():
    logger.info("main")
    database_dir = "database\parameters_0.csv"
    DBH = DataBaseHandler(database_dir)
    DBH.read_database()
    DBH.data_adder(120, 120, 27.5, 6.5)
    DBH.data_adder(120, 120, 33.75, 6.5)
    DBH.write_database()

if __name__ == "__main__":
    logger = csu_logger.logger_init()
    main()