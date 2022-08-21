import pandas as pd 
import numpy as np


pkl_path = "template\\test_5.pkl"

df = pd.read_pickle(pkl_path)
print(df)


columns=['side_c', 'side_d', 'height','radius', 'hash_id','generated']

data = np.array([[80.0, 10.0, 10.0, 5.0, "val_3_80.0x10.0x10.0_R3.0", "0"]])

test_df = pd.DataFrame(data, columns=columns)
print(test_df)
test_pkl_path = 'template\\valid_set_0.pkl'

test_df.to_pickle(test_pkl_path)

df = pd.read_pickle(test_pkl_path)
print(df)