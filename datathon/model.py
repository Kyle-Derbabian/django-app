import pandas as pd

df = pd.read_csv("datathon/NYPD_Hate_Crimes.csv")
df.dropna(inplace=True)
df.reset_index(inplace=True)
num_rows, num_cols = df.shape

print(df)
print(num_rows, num_cols)
