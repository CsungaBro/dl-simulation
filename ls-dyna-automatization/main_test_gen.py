import pandas as pd 
import numpy as np


pkl_path = "template\\test_5.pkl"

df = pd.read_pickle(pkl_path)
print(df)


columns=['side_c', 'side_d', 'height','radius', 'hash_id','generated']

data = np.array([[20.0, 20.0, 20.0, 10.0, "val_0_20.0x20.0x20.0_R10.0", "0"]])

test_df = pd.DataFrame(data, columns=columns)
print(test_df)
test_pkl_path = 'template\\valid_set_0.pkl'

test_df.to_pickle(test_pkl_path)

df = pd.read_pickle(test_pkl_path)
print(df)