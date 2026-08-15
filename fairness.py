import pandas as pd

df = pd.read_csv("EYOUTH-31103161200834-Library-task2_cleaned_data.csv")

checkouts_per_hood = df['neighborhood'].value_counts()
members_per_hood = df.groupby('neighborhood')['member_id'].nunique()

comparison = pd.DataFrame({
    'Total Members': members_per_hood,
    'Total Checkouts': checkouts_per_hood
}).fillna(0)

print("--- Neighborhood Comparison ---")
print(comparison)