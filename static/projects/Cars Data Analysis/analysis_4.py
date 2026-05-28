"""
Create price categories based on MSRP ranges
and assign labels like Budget, Premium,and
Luxury to better analyze car price segments
"""

msrp_bins = [0, 20000, 40000, 70000, 120000, 2200000]
msrp_labels =[
  'Budget', 'Mid Range', 'Premium',
  'Luxury', 'Ultra Luxury'
]

df['Price_Group'] = pd.cut(
  df['MSRP'], bins=msrp_bins, labels=msrp_labels
)

# Checking minimum and maximum MSRP value 
df["MSRP"].agg(['min', 'max'])
