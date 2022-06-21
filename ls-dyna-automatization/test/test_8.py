import pandas as pd
import numpy as np

pck_path = 'test\\test_test.pkl'

df = pd.read_pickle(pck_path)

print(df)
print(df.index)
print(df.index[0])

df_2 =  df.iloc[np.random.permutation(len(df))]
print(df_2)