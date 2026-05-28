import pandas as pd

# Main Function to Load Data
def load_data(database):
    df = pd.read_csv(database)
    
data = "Cars_data.csv"
load_data(data)

df.tail(20)

# Display Last 20 rows of Dataset 
