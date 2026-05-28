import pandas as pd

def load_data(database):
    df = pd.read_csv(database)
    
data = "Cars_data.csv"
load_data(data)

df.head(20)
