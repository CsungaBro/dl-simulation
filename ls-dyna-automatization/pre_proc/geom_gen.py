import regex as re
import os 
import logging
import pandas as pd


class GeometricParameters:
    """
    Create the geometry parameters for the simulation. 
    The main_parameters are generated from main_parameters_ranges with the number of simulations specified. 
    From the main_parameters the derived_parameters are generated. 
    """
    def __init__(self, pkl_path, number_of_sims):
        self.pkl_path = pkl_path
        base_df = pd.read_pickle(pkl_path)
        logging.info(base_df.head(n=12))
        self.number_of_sims= number_of_sims        
        self.df = base_df[base_df["generated"] != '1']
        self.df['side_c'] = self.df['side_c'].astype('float64')
        self.df['side_d'] = self.df['side_d'].astype('float64')
        self.df['height'] = self.df['height'].astype('float64')
        self.df['radius'] = self.df['radius'].astype('float64')       
        logging.info(self.df.head())
        self.simulations_currently_in_container = 0
        self.fix_parameters = {
            # base parameters
            "formschraege" : 2, # Grad
            "thickness" : 2,
            "z0" : 10,
            # Stamp/Stempel parameters        
            "mesh_max_1" : 3,
            # Matrize parameters
            "r2_u" : 3,
            "mesh_max_2" : 6,
            # Organoblech parameters
            "mesh_max_3" : 3,
            "mesh_min_3" : 1,
            "mesh_dev_3" : 0.5
        }
        self.main_parameters = {}
        self.derived_parameters = {}
        self.all_parameters = {}
        self.all_parameters_container = []
        self.parameters_generated = 0

    def calculate_main_parameters(self, row_number):
        """
        Calculates the main parameters based on the range given in the "main_parameters_range"
        """
        self.main_parameters["c2"]=self.df.iloc[row_number, 0]
        self.main_parameters["d2"]=self.df.iloc[row_number, 1]
        self.main_parameters["h2"]=self.df.iloc[row_number, 2]
        self.main_parameters["r2_b"]=self.df.iloc[row_number, 3]
        self.main_parameters["sim_id"]=self.df.index[row_number]

    def check_if_doable_geom(self):
        """
        Checks if the geometry with the given parameters is doable
        ->If the sum of the two radius is smaller then the height of the Matrice
        -> If the radius in the "Stempel" larger then 0
        """
        sum_radius = self.main_parameters["r2_b"]+self.fix_parameters["r2_u"]

        if sum_radius+1 > self.main_parameters["h2"] or self.derived_parameters["r1"] <=0:
            return False
        else:
            return True

    def calculate_derived_parameters(self):
        """
        Calculates the derived parameters based on the main parameters
        """
        # Helper parameters
        top_part_length = self.main_parameters["h2"]-(self.main_parameters["r2_b"]+self.fix_parameters["r2_u"])
        perimeter = (self.main_parameters["r2_b"]+self.fix_parameters["r2_u"])*3.1415/2
        self.derived_parameters["h1"] = self.main_parameters["h2"]+5
        self.derived_parameters["z1"] = self.main_parameters["h2"]+self.fix_parameters["z0"]+self.fix_parameters["thickness"]
        self.derived_parameters["a1"] = self.main_parameters["c2"]-self.fix_parameters["thickness"]
        self.derived_parameters["b1"] = self.main_parameters["d2"]-self.fix_parameters["thickness"]
        self.derived_parameters["r1"] = self.main_parameters["r2_b"]-self.fix_parameters["thickness"]
        self.derived_parameters["way1"] = self.main_parameters["h2"]
        self.derived_parameters["mesh_max_1"] = (self.main_parameters["c2"] + self.main_parameters["d2"]) / (2*1.5*10)
        self.derived_parameters["mesh_min_1"] = self.derived_parameters["mesh_max_1"] / 2
        self.derived_parameters["mesh_dev_1"] = self.derived_parameters["mesh_min_1"] / 2
        self.derived_parameters["mesh_dev_1"] = round(self.derived_parameters["mesh_max_1"], 2)
        self.derived_parameters["mesh_dev_1"] = round(self.derived_parameters["mesh_min_1"], 2)
        self.derived_parameters["mesh_dev_1"] = round(self.derived_parameters["mesh_dev_1"], 2)
        # Matrize parameters
        self.derived_parameters["z2"] = self.main_parameters["h2"]+self.fix_parameters["z0"]
        self.derived_parameters["a2"] = self.main_parameters["c2"]+top_part_length+perimeter+10
        self.derived_parameters["b2"] = self.main_parameters["d2"]+top_part_length+perimeter+10
        self.derived_parameters["mesh_max_2"] = (self.main_parameters["c2"] + self.main_parameters["d2"]) / (2*1.5*10)
        self.derived_parameters["mesh_min_2"] = self.derived_parameters["mesh_max_2"] / 2
        self.derived_parameters["mesh_dev_2"] = self.derived_parameters["mesh_min_2"] / 2
        self.derived_parameters["mesh_dev_2"] = round(self.derived_parameters["mesh_max_2"], 2)
        self.derived_parameters["mesh_dev_2"] = round(self.derived_parameters["mesh_min_2"], 2)
        self.derived_parameters["mesh_dev_2"] = round(self.derived_parameters["mesh_dev_2"], 2)
        # Organoblech parameters
        self.derived_parameters["a3"] = self.main_parameters["c2"]-self.main_parameters["r2_b"]+top_part_length+perimeter+5
        self.derived_parameters["b3"] = self.main_parameters["d2"]-self.main_parameters["r2_b"]+top_part_length+perimeter+5
        self.derived_parameters["z3"] = self.main_parameters["h2"]+self.fix_parameters["z0"]+self.fix_parameters["thickness"]/2
        self.derived_parameters["mesh_max_3"] = (self.main_parameters["c2"] + self.main_parameters["d2"]) / (2*1.5*10)
        self.derived_parameters["mesh_min_3"] = self.derived_parameters["mesh_max_3"] / 2
        self.derived_parameters["mesh_dev_3"] = self.derived_parameters["mesh_min_3"] / 2
        self.derived_parameters["mesh_dev_3"] = round(self.derived_parameters["mesh_max_3"], 2)
        self.derived_parameters["mesh_dev_3"] = round(self.derived_parameters["mesh_min_3"], 2)
        self.derived_parameters["mesh_dev_3"] = round(self.derived_parameters["mesh_dev_3"], 2)
    
    def calculate_all_parameters(self, row):
        """
        Calculates all of the parameters, than if the geometry is doable saves it in a container
        """
        self.all_parameters = {}
        self.calculate_main_parameters(row)
        c, d, h, r = self.main_parameters["c2"], self.main_parameters["d2"], self.main_parameters["h2"], self.main_parameters["r2_b"]
        hash_id = self.df.iloc[row, 4]
        hash_dict = {'hash_id': hash_id}
        # The problem is somewhere here
        logging.debug(hash_id)
        self.calculate_derived_parameters()
        self.all_parameters.update(self.main_parameters)
        self.all_parameters.update(self.derived_parameters)
        self.all_parameters.update(self.fix_parameters)
        self.all_parameters.update(hash_dict)

    def generate_all_parameters(self):
        """
        Generates all of the variations of the parameters for the simulation
        """
        logging.info(self.number_of_sims)
        for row in range(self.number_of_sims):
                self.calculate_all_parameters(row)
                self.all_parameters_container.append(self.all_parameters)
                logging.info("Generated")
                self.df.iloc[row, 5] = '1' #THIS
        self.df.to_pickle(self.pkl_path)


class OutputNameGenerator:
    """
    From the list of parameters, use the length, width, and 
    roundness of the matrix to create paths for each simulation.
    """
    def __init__(self, output_path, all_parameters_cointainer):
        self.output_path = output_path
        self.all_parameters_cointainer = all_parameters_cointainer
        self.output_names = []

    def hash_id_generator(self, side_c, side_d, height, radius):
        side_c = round(side_c, 5)
        side_d = round(side_d, 5)
        height = round(height, 5)
        radius = round(radius, 5)
        return f"{side_c}x{side_d}x{height}_R{radius}"    

    def output_path_generator(self):
        for count, parameters in enumerate(self.all_parameters_cointainer):
            c, d, h, r, sim_id = parameters["c2"], parameters["d2"], parameters["h2"], parameters["r2_b"], parameters["sim_id"]
            # hash_data = self.MySQLHandler.hash_data_maker(c, d, h, r)
            # sim_name = self.MySQLHandler.data_getter_handler(hash_data)
            sim_name = parameters["hash_id"]
            # logging.info(f"sim_name in geom_gen: {sim_name}")
            file_name = f"{sim_name}.cfile"
            logging.info(f"file_name in geom_gen: {file_name} and {count}. file")
            self.output_names.append(os.path.join(self.output_path, file_name))


class KFileSaveHandling():
    """
    Edits the K-File's "R way1" Paramater
    """
    def __init__(self, all_parameters_cointainer, output_names):
        self.all_parameters_cointainer = all_parameters_cointainer
        self.output_names = output_names
    
    def generate_all_k_file(self):
        for output_path, parameters in zip(self.output_names, self.all_parameters_cointainer):
            self.parameters = parameters
            self.generate_k_file(output_path)

    def generate_give_k_file(self, k_file_path, count):
        self.parameters = self.all_parameters_cointainer[count]
        self.generate_k_file(k_file_path)        

    def generate_k_file(self, output_path):
        content = ""
        with open(output_path,"r") as f_r:
            for line in f_r:
                content += self.process(line, output_path)
        with open(output_path,"w") as f_w:
                f_w.write(content)        

    def process(self, line, output_path):
        if bool(re.search("R way1", line)):
            h_par = re.findall("x[0-9]+.[0-9]+_", output_path)[0]
            h_float = float(h_par[1:-1])
            h_line = f"R way1    {h_float}  \n"
            return h_line 
        return line


class CFileHandling():
    """
    It generates .cfiles one by one from a list of parameters.
    It takes as input the parameters generated by GeometricParameters, 
    the paths generated by OutputNameGenerator and a sample .cfile.
    """
    def __init__(self, generator_file, all_parameters_cointainer, output_names):
        self.generator_file = generator_file
        self.geom_part = True
        self.all_parameters_cointainer = all_parameters_cointainer
        self.output_names = output_names
        self.parameters = {}

    def generate_c_file(self, output_file):
        with open(self.generator_file, "r") as f_r, open(output_file,"w") as f_w:
            for line in f_r:
                f_w.write(self.process(line))
        self.geom_part = True

    def process(self,line):
        if not self.geom_part:
            return line
        if "KEYWORD INPUT 1" in line:
            self.geom_part = False
            return line
        new_line = line
        for parameter in self.parameters.keys():
            if parameter in new_line:
                new_line = re.sub(parameter,str(self.parameters[parameter]),new_line)
        return new_line

    def generate_all_c_file(self):
        for output_path, parameters in zip(self.output_names, self.all_parameters_cointainer):
            self.parameters = parameters
            self.generate_c_file(output_path)


if __name__ == "__main__":
    # input_file = "ls-dyna-automatization\\template\\save_2.cfile"
    # output_file = "ls-dyna-automatization\\output"
    input_file = "template\\save_2.cfile"
    output_path = "output\\c_files"
    parameters_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\template\\test.pkl"
    
    # height_range = [5,30]
    # radius_range = [2,20]
    # number_of_simulation = 5

    P = GeometricParameters(parameters_path)
    P.generate_all_parameters()
    ONG = OutputNameGenerator(output_path, P.all_parameters_container)
    ONG.output_path_generator()
    CFH = CFileHandling(input_file, P.all_parameters_container, ONG.output_names)
    CFH.generate_all_c_file()
    KFH = KFileSaveHandling(P.all_parameters_container, ONG.output_names)
    KFH.generate_all_k_file()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
'''
PROBLEM FOUND
--> Somehow the generator doesnt gives back the right params and then it cant find in the SQL db
'''