import json
import pandas as pd

f1 = pd.read_json('harvey_weinstein.json')
f2 = pd.read_json('harvey_weinstein_0.json')
f3 = pd.read_json('harvey_weinstein_0.json')

frames = [f1, f2, f3]

result = pd.concat(frames)
result.drop_duplicates()

result.to_pickle('harvey_weinstein.pkl')