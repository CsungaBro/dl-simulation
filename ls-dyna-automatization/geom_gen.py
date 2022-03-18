import regex as re

class Parameters():
    def __init__(self):
        # base parameters
        self.z0 = 10
        # Stamp/Stempel parameters
        self.z1 = 15 + self.z0 
        self.z1_abs = 33
        self.a1 = 58
        self.b1 = 58
        self.ra1 = 10
        self.mesh_max_1 = 6
        self.mesh_min_1 = 2
        self.mesh_dev_1 = 1
        # Matrize parameters
        self.z2 = 20
        self.z2_abs = self.z2 + self.z0 
        self.a2 = 60
        self.b2 = 60
        self.c2 = 60
        self.d2 = 60
        self.ra2 = 10
        self.rc2 = 5
        self.mesh_max_2 = 3
        self.mesh_min_2 = 1
        self.mesh_dev_2 = 0.5
        # Organoblech parameters
        self.a3 = 80
        self.b3 = 80
        self.z3 = 33
        self.mesh_max_2 = 3
        self.mesh_min_2 = 1
        self.mesh_dev_2 = 0.5    

        

class Main():
    def __init__(self,generator_file,output_file):
        self.generator_file = generator_file
        self.output_file = output_file
        self.par = vars(Parameters)
        self.geom_part = True
        self.parameters = {
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

    def file_reader(self):
        with open(self.generator_file, "r") as f_r, open(self.output_file,"w") as f_w:
            for line in f_r:
                f_w.write(self.process(line))

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
    M = Main(input_file, output_file)
    M.file_reader()