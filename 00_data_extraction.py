import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.oauth2 import service_account
from google.cloud import bigquery

import warnings
warnings.filterwarnings("ignore")

print('Finished importing modules.')

credentials = service_account.Credentials.from_service_account_file('/Users/andrescervantes/Documents/xepelin-acn/xepelin-ds-test-151da8f0658b.json')
client = bigquery.Client(credentials=credentials, project='xepelin-ds-prod')

q = f'''
select *
from `xepelin-ds-test.dbt_acervantes_squad_bi_analytics.ParentChildEntities`
'''

df = client.query(q).to_dataframe()

df['parentTotalAmountFinanced'] = pd.to_numeric(df['parentTotalAmountFinanced'])
df['parentCreditLineAvailable'] = pd.to_numeric(df['parentCreditLineAvailable'])
df['childTotalAmountFinanced'] = pd.to_numeric(df['childTotalAmountFinanced'])
df['childCreditLineAvailable'] = pd.to_numeric(df['childCreditLineAvailable'])

df.to_csv('data.csv')

print('Finished running script.')