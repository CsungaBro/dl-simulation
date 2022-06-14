import pandas as pd
import numpy as np
import logging
from math import sqrt
import itertools


class ParamaterGeneretor:
    def __init__(self, height_range, radius_range, side_c_range, side_d_range, fix_radius) -> None:
        self.side_c_range = side_c_range
        self.side_d_range = side_d_range
        self.height_range = height_range
        self.radius_range = radius_range
        self.fix_radius = fix_radius
        self.safety = 1
        self.number_of_generated = 0
        self.i = 0
        self.datafrate_init()
    
    def datafrate_init(self):
        # minimum parameter calculation
        radius_min = self.radius_range[0]
        side_c_min_opt = 2*radius_min + self.safety 
        side_d_min_opt = 2*radius_min + self.safety
        height_min_opt =  radius_min + self.fix_radius + self.safety
        # checking if the give minimum or the calculated minimum is feasible
        side_c_min =side_c_min_opt if side_c_min_opt > self.side_c_range[0] else self.side_c_range[0] 
        side_d_min =side_d_min_opt if side_d_min_opt > self.side_d_range[0] else self.side_d_range[0]
        height_min =height_min_opt if height_min_opt > self.height_range[0] else self.height_range[0]        
        # maximum parameter calculation
        height_max = self.height_range[1] 
        radius_max_opt = height_max - self.fix_radius - self.safety
        # checking if the give minimum or the calculated maximum is feasible
        radius_max = radius_max_opt if radius_max_opt < self.radius_range[1] else self.radius_range[1]
        side_c_max = self.side_c_range[1]
        side_d_max = self.side_d_range[1]
        #init of the dataframe
        hash_id_min = self.hash_id_generator(side_c_min, side_d_min, height_min, radius_min)
        hash_id_max = self.hash_id_generator(side_c_max, side_d_max, height_max, radius_max)
        data = np.array([
            [side_c_min, side_d_min, height_min, radius_min, hash_id_min, 0],
            [side_c_max, side_d_max, height_max, radius_max, hash_id_max, 0]])
        self.df = pd.DataFrame(data, columns=['side_c', 'side_d', 'height','radius', 'hash_id', 'generated'])
        self.df['side_c'] = self.df['side_c'].astype('float64')
        self.df['side_d'] = self.df['side_d'].astype('float64')
        self.df['height'] = self.df['height'].astype('float64')
        self.df['radius'] = self.df['radius'].astype('float64')
        print(self.df.head())


    def implementation_check(self, side_c, side_d, height, radius):
        max_radius = radius + self.fix_radius + self.safety
        max_side_radius = 2*radius + self.safety
        if height < max_radius:
            return False
        if side_c < max_side_radius or side_d <max_side_radius:
            return False
        return True

    def all_parameter_generator(self, number_of_simulations, pkl_path):
        needed_var = int(number_of_simulations**(1/4))
        lists = self.possible_numbers_generator(needed_var)
        for i in range(needed_var):
            for j in range(needed_var):
                print(self.df)
                for k in range(needed_var):
                    for l in range(needed_var):
                        side_c = lists[0][i]
                        side_d = lists[1][j]
                        height = lists[2][k]
                        radius = lists[3][l]
                        self.parameter_generator(side_c, side_d, height, radius)
        self.df.to_pickle(pkl_path)
        print(self.df)
    
    def step_generator(self, par_min, par_max, needed_var):
        diff = par_max-par_min
        step = diff / needed_var
        return step

    def possible_numbers_generator(self, needed_var):
        side_c_step = self.step_generator(self.df.iloc[-2, 0], self.df.iloc[-1, 0], needed_var)
        side_d_step = self.step_generator(self.df.iloc[-2, 1], self.df.iloc[-1, 1], needed_var)
        height_step = self.step_generator(self.df.iloc[-2, 2], self.df.iloc[-1, 2], needed_var)
        radius_step = self.step_generator(self.df.iloc[-2, 3], self.df.iloc[-1, 3], needed_var)
        side_c_nums = [self.df.iloc[-2, 0]+x*side_c_step for x in range(needed_var-1)]
        side_d_nums = [self.df.iloc[-2, 1]+x*side_d_step for x in range(needed_var-1)]
        height_nums = [self.df.iloc[-2, 2]+x*height_step for x in range(needed_var-1)]
        radius_nums = [self.df.iloc[-2, 3]+x*radius_step for x in range(needed_var-1)]
        side_c_nums.append(self.df.iloc[-1, 0])
        side_d_nums.append(self.df.iloc[-1, 1])
        height_nums.append(self.df.iloc[-1, 2])
        radius_nums.append(self.df.iloc[-1, 3])
        print(f"side_c_nums: {side_c_nums}")
        print(f"side_d_nums: {side_d_nums}")
        print(f"height_nums: {height_nums}")
        print(f"radius_nums: {radius_nums}")
        return [side_c_nums, side_d_nums, height_nums, radius_nums]
        
    def hash_id_generator(self, side_c, side_d, height, radius):
        side_c = round(side_c, 5)
        side_d = round(side_d, 5)
        height = round(height, 5)
        radius = round(radius, 5)
        return f"{side_c}x{side_d}x{height}_R{radius}"

    def parameter_generator(self, side_c, side_d, height, radius):
        if self.implementation_check(side_c, side_d, height, radius):
            hash_id = self.hash_id_generator(side_c, side_d, height, radius)
            data = np.array([[side_c, side_d, height, radius, hash_id, 0]])
            new_df = pd.DataFrame(data, columns=['side_c', 'side_d', 'height','radius', 'hash_id', 'generated'])
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.number_of_generated = self.number_of_generated + 1
        else:
            print("NOT Added")


    def old_parameter_generator(self):
        last_two_row = self.df.iloc[[-2,-1], :]
        print(last_two_row)
        mean_of_df = last_two_row.mean()
        print(mean_of_df) 
        side_c = mean_of_df['side_c']
        side_d = mean_of_df['side_d']
        height = mean_of_df['height']
        radius = mean_of_df['radius']
        print(side_c, side_d, height, radius)
        if self.implementation_check(side_c, side_d, height, radius):
            data = np.array([[side_c, side_d, height, radius]])
            new_df = pd.DataFrame(data, columns=['side_c', 'side_d', 'height','radius'])
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self.number_of_generated = self.number_of_generated + 1
        

if __name__ == '__main__':
    parameters_dic = {
        "number_of_simulations" : 20_000, # BUG not sim but case in for the main params
        # Matrize parameters
        "h2" : [5, 20],# "z2_int" = 5-30,
        "r2_b" : [2, 15], # "ra2_int" = ~2/3/5-30
        'c2' : [20, 80],
        'd2' : [20, 80],
        }
    fix_params = {
        'r2_u' : 3
    }
    number_of_simulations =parameters_dic['number_of_simulations']
    height_range = parameters_dic['h2']
    radius_range = parameters_dic['r2_b']
    side_c_range = parameters_dic['c2']
    side_d_range = parameters_dic['d2']
    fix_radius = fix_params['r2_u']
    paramater_generetor = ParamaterGeneretor(height_range, radius_range, side_c_range, side_d_range, fix_radius)
    pkl_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\template\\test.pkl"
    paramater_generetor.all_parameter_generator(number_of_simulations, pkl_path)