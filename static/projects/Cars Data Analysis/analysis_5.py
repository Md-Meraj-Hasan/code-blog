"""
Create horsepower categories based on
engine power ranges to classify
vehicles into Low, Medium, High,
and Extreme performance groups
"""

hp_bins = [0, 150, 250, 400, 1002]
hp_labels = [
  'Low Power', 'Medium Power',
  'High Power', 'Extreme Power'
]

df['Engine_HP_Group'] = pd.cut(
df["Engine HP"], bins=hp_bins, labels=hp_labels
  )

# Display Minimum and Maximum Horsepower Value
df["Engine HP"].agg(["min", "max"])
