#%%
import pandas as pd
import json

with open('runs_giles.json', 'r') as f:
    data = json.load(f)

df = pd.json_normalize(data)
#%%

experiment = df[df["attempt_name"]=="getting_it_working_1"]
experiment[["model_config.temprature","answer","expectation"]].groupby(["model_config.temprature"]).value_counts()

# %%
