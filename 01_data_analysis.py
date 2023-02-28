import pandas as pd

import functions as ff

# df = pd.read_csv('data.csv')

parent_df = ff.build_summary_row('MMI050520B15')

print(parent_df.head())