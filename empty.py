import pandas as pd
df = pd.read_csv('passwords batch.csv')
df = df.iloc[0:0]

df.to_csv('passwords batch.csv', index=False)