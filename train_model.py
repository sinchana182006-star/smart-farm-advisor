import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.read_csv("data.csv")

X = data[['N','P','K','temperature','humidity','ph','rainfall']]
y = data['label']

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("✅ model.pkl created")