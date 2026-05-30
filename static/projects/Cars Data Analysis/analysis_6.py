"""
City MPG (Miles Per Gallon) ko mileage
categories me divide kar rahe hain.
"""

hp_bins = [0, 20, 40, 70, 140]
mpg_labels = [
  'Performance/Heavy','Daily Cummuter',
  'Economy/Hybrid', 'Electric/EV'
]

df['City_mpg_Group'] = pd.cut(
df["city mpg"], bins=mpg_bins,
  labels=mpg_labels
)

# checking city mpg:  min aur max value
df["city mpg"].agg(["min", "max"])
