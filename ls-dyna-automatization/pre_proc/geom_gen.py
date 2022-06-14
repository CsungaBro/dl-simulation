import regex as re
import os 
import logging


class GeometricParameters():
    """
    Create the geometry parameters for the simulation. 
    The main_parameters are generated from main_parameters_ranges with the number of simulations specified. 
    From the main_parameters the derived_parameters are generated. 
    """
    def __init__(self, height_range, radius_range, number_of_simulation, MySQLHandler):
        self.MySQLHandler = MySQLHandler
        self.main_parameters_range = {
            "number_of_simulations" : number_of_simulation, # BUG not sim but case in for the main params
            # Matrize parameters
            "h2" : height_range,# "z2_int" = 5-30,
            "r2_b" : radius_range, # "ra2_int" = ~2/3/5-30
            }
        self.simulations_currently_in_container = 0
        self.fix_parameters = {
            # base parameters
            "formschraege" : 2, # Grad
            "thickness" : 2,
            "z0" : 10,
            # Stamp/Stempel parameters        
            "mesh_max_1" : 3,
            "mesh_min_1" : 1,
            "mesh_dev_1" : 0.5,
            # Matrize parameters
            "a2" : 120,
            "b2" : 120,
            "c2" : 50,
            "d2" : 50,
            "r2_u" : 3,
            "mesh_max_2" : 6,
            "mesh_min_2" : 2,
            "mesh_dev_2" : 1,
            # Organoblech parameters
            "mesh_max_3" : 3,
            "mesh_min_3" : 1,
            "mesh_dev_3" : 0.5
        }
        self.main_parameters = {}
        self.derived_parameters = {}
        self.all_parameters = {}
        self.all_parameters_container = []

    def calculate_main_parameters(self, var_1, var_2):
        """
        Calculates the main parameters based on the range given in the "main_parameters_range"
        """
        if self.main_parameters_range["number_of_simulations"] == 1:
            self.main_parameters["h2"]=self.main_parameters_range["h2"][0]
            self.main_parameters["r2_b"]=self.main_parameters_range["r2_b"][0]
        else:
            nof = self.main_parameters_range["number_of_simulations"]
            step_h2 = (self.main_parameters_range["h2"][1]-self.main_parameters_range["h2"][0])/(nof-1)
            step_r2_b = (self.main_parameters_range["r2_b"][1]-self.main_parameters_range["r2_b"][0])/(nof-1)
            self.main_parameters["h2"]=self.main_parameters_range["h2"][0]+var_1*step_h2
            self.main_parameters["r2_b"]=self.main_parameters_range["r2_b"][0]+var_2*step_r2_b

    def check_if_doable_geom(self):
        """
        Checks if the geometry with the given parameters is doable
        ->If the sum of the two radius is smaller then the height of the Matrice
        -> If the radius in the "Stempel" larger then 0
        """
        sum_radius = self.main_parameters["r2_b"]+self.fix_parameters["r2_u"]

        if sum_radius+2 >= self.main_parameters["h2"] or self.derived_parameters["r1"] <=0:
            return False
        else:
            return True

    def calculate_derived_parameters(self):
        """
        Calculates the derived parameters based on the main parameters
        """
        self.derived_parameters["h1"] = self.main_parameters["h2"]+5
        self.derived_parameters["z1"] = self.main_parameters["h2"]+self.fix_parameters["z0"]+self.fix_parameters["thickness"]
        self.derived_parameters["a1"] = self.fix_parameters["c2"]-self.fix_parameters["thickness"]
        self.derived_parameters["b1"] = self.fix_parameters["d2"]-self.fix_parameters["thickness"]
        self.derived_parameters["r1"] = self.main_parameters["r2_b"]-self.fix_parameters["thickness"]
        self.derived_parameters["way1"] = self.main_parameters["h2"]
        # Matrize parameters
        self.derived_parameters["z2"] = self.main_parameters["h2"]+self.fix_parameters["z0"]
        # Organoblech parameters
        top_part_length = self.main_parameters["h2"]-(self.main_parameters["r2_b"]+self.fix_parameters["r2_u"])
        perimeter = (self.main_parameters["r2_b"]+self.fix_parameters["r2_u"])*3.1415/2
        self.derived_parameters["a3"] = self.fix_parameters["c2"]-self.main_parameters["r2_b"]+top_part_length+perimeter+5
        self.derived_parameters["b3"] = self.fix_parameters["d2"]-self.main_parameters["r2_b"]+top_part_length+perimeter+5
        self.derived_parameters["z3"] = self.main_parameters["h2"]+self.fix_parameters["z0"]+self.fix_parameters["thickness"]/2
    
    def calculate_all_parameters(self, var_1, var_2):
        """
        Calculates all of the parameters, than if the geometry is doable saves it in a container
        """
        self.all_parameters = {}
        self.calculate_main_parameters(var_1, var_2)
        c, d, h, r = self.fix_parameters["c2"], self.fix_parameters["d2"], self.main_parameters["h2"], self.main_parameters["r2_b"]
        hash_id = self.MySQLHandler.hash_data_maker(c, d, h, r)
        # The problem is somewhere here
        logging.debug(hash_id)
        if not self.MySQLHandler.already_added_checker(hash_id):
            logging.debug("IN")
            self.calculate_derived_parameters()
            if self.check_if_doable_geom():
                self.all_parameters.update(self.main_parameters)
                self.all_parameters.update(self.derived_parameters)
                self.all_parameters.update(self.fix_parameters)
                self.MySQLHandler.data_setter_handler(c, d, h, r)
                return True 
        else:
            return False

    def generate_all_parameters(self):
        """
        Generates all of the variations of the parameters for the simulation
        """
        for var_1 in range(self.main_parameters_range["number_of_simulations"]):
            for var_2 in range(self.main_parameters_range["number_of_simulations"]):
                is_it_new = self.calculate_all_parameters(var_1, var_2)
                if is_it_new:
                    if self.check_if_doable_geom():
                        self.all_parameters_container.append(self.all_parameters)
                        logging.info("Generated")


class OutputNameGenerator:
    """
    From the list of parameters, use the length, width, and 
    roundness of the matrix to create paths for each simulation.
    """
    def __init__(self, output_path, all_parameters_cointainer, MySQLHandler):
        self.MySQLHandler = MySQLHandler
        self.output_path = output_path
        self.all_parameters_cointainer = all_parameters_cointainer
        self.output_names = []

    def output_path_generator(self):
        for count, parameters in enumerate(self.all_parameters_cointainer):
            c, d, h, r = parameters["c2"], parameters["d2"], parameters["h2"], parameters["r2_b"]
            logging.error(f"params in geom_gen{c}, {d}, {h}, {r}")
            # hash_data = self.MySQLHandler.hash_data_maker(c, d, h, r)
            # sim_name = self.MySQLHandler.data_getter_handler(hash_data)
            sim_name = self.MySQLHandler.data_getter_handler(c, d, h, r)
            logging.info(f"sim_name in geom_gen: {sim_name}")
            file_name = f"{sim_name}.cfile"
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
                content += self.process(line)
        with open(output_path,"w") as f_w:
                f_w.write(content)        

    def process(self, line):
        if bool(re.search("R way1", line)):
            return "R way1    {}  \n".format(self.parameters["way1"])
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
    
    height_range = [5,30]
    radius_range = [2,20]
    number_of_simulation = 5

    P = GeometricParameters(height_range, radius_range, number_of_simulation)
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