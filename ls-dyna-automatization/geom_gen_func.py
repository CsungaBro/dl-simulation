import regex as re

class Geometric_Parameters():
    def __init__(self):
        self.main_parameters_range = {}
        self.main_parameters = {
        # base parameters
        "z0" : 10,
        # Stamp/Stempel parameters
        "h1" : 15 ,
        "z1" : 33,
        "a1" : 48,
        "b1" : 48,
        "r1" : 10,
        "mesh_max_1" : 3,
        "mesh_min_1" : 1,
        "mesh_dev_1" : 0.5,
        # Matrize parameters
        "h2" : 20,
        "z2" : 30 ,
        "a2" : 120,
        "b2" : 120,
        "c2" : 50,
        "d2" : 50,
        "r2_u" : 5,
        "r2_b" : 10,
        "mesh_max_2" : 6,
        "mesh_min_2" : 2,
        "mesh_dev_2" : 1,
        # Organoblech parameters
        "a3" : 80,
        "b3" : 80,
        "z3" : 31,
        "mesh_max_3" : 3,
        "mesh_min_3" : 1,
        "mesh_dev_3" : 0.5}
        self.derived_parameters = {}
        self.all_parameters = {}
        self.all_parameters_container = []

        self.main()

    def calculate_main_parameters(self):
        pass

    def calculate_derived_parameters(self):
        pass

    def main(self):
        self.all_parameters.update(self.main_parameters)
        self.all_parameters.update(self.derived_parameters)
        self.all_parameters_container.append(self.all_parameters)

class Main():
    def __init__(self,generator_file, output_file, all_parameters_cointainer):
        self.generator_file = generator_file
        self.output_file = output_file
        self.output_names = []
        self.geom_part = True
        self.all_params_array = all_parameters_cointainer
        self.parameters = {}
        # self.parameters = {
        # # base parameters
        # "z0" : 10,
        # # Stamp/Stempel parameters
        # "h1" : 15 ,
        # "z1" : 33,
        # "a1" : 48,
        # "b1" : 48,
        # "r1" : 10,
        # "mesh_max_1" : 3,
        # "mesh_min_1" : 1,
        # "mesh_dev_1" : 0.5,
        # # Matrize parameters
        # "h2" : 20,
        # "z2" : 30 ,
        # "a2" : 120,
        # "b2" : 120,
        # "c2" : 50,
        # "d2" : 50,
        # "r2_u" : 5,
        # "r2_b" : 10,
        # "mesh_max_2" : 6,
        # "mesh_min_2" : 2,
        # "mesh_dev_2" : 1,
        # # Organoblech parameters
        # "a3" : 80,
        # "b3" : 80,
        # "z3" : 31,
        # "mesh_max_3" : 3,
        # "mesh_min_3" : 1,
        # "mesh_dev_3" : 0.5}        

    def dict_getter(self):
        self.parameters = self.all_params_array[0]

    def generate_c_file(self):
        with open(self.generator_file, "r") as f_r, open(self.output_file,"w") as f_w:
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
    
if __name__ == "__main__":
    # input_file = "ls-dyna-automatization\\template\\k_file_gen.cfile"
    input_file = "ls-dyna-automatization\\template\\save_2.cfile"
    output_file = "ls-dyna-automatization\\output\\test2.cfile"

    P = Geometric_Parameters

    M = Main(input_file, output_file, P.all_parameters_container)
    M.generate_c_file()