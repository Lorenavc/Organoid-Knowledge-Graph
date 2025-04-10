import pandas as pd

# Load your dataset
my_data = pd.read_csv("ArrayExpress_metadata.csv")

# Load PrimeKG dataset
primekg = pd.read_csv("kg.csv", low_memory=False) # Replace 'kg.csv' with your csv file path to your own knowledge graph data or metadata

# Filter PrimeKG to keep only rows where x_name (unidirectional) appears in our csv's perturbagen and organ columns
filtered_primekg = primekg[
    (primekg["x_name"].isin(my_data["perturbagen"])) |    # Replace 'x_name' with the column name in your KG that should match 'perturbagen' in your metadata
    (primekg["x_name"].isin(my_data["organ"]))            # Replace 'x_name' with the column name in your KG that should match 'organ' in your metadata
# If interested in other columns in Organoid KG, replace 'perturbagen' and/or 'organ' with other Organoid KG column names (refer to ArrayExpress_metadata.csv)
]

# Save the filtered dataset
filtered_primekg.to_csv("uni_filt_primekg.csv", index=False)    # Replace with preferred file name
print(f"Filtered PrimeKG size: {filtered_primekg.shape}")
