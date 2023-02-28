import sys

import pandas as pd

import funcs as ff

#sys.path.insert(0, '/functions/')

# df = pd.read_csv('data.csv')

parent_df = ff.build_summary_row('ZUNR780720KU9')

print(parent_df.head())