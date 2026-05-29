import pandas as pd

# Main Function to Data Load
def load_data(database):
    df = pd.read_csv(database)
    return df
    
data = "Cars_data.csv"
df = load_data(data)

df.head(20)

# Display First 20 rows of Dataset 
