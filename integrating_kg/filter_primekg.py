import pandas as pd

# Load your dataset
my_data = pd.read_csv("ArrayExpress_metadata.csv")

# Load PrimeKG dataset
primekg = pd.read_csv("kg.csv", low_memory=False)

# Filter PrimeKG to keep only rows where x_name (unidirectional) appears in our csv's perturbagen and organ columns
filtered_primekg = primekg[
    (primekg["x_name"].isin(my_data["perturbagen"])) |
    (primekg["x_name"].isin(my_data["organ"]))
]

# Save the filtered dataset
filtered_primekg.to_csv("uni_filt_primekg.csv", index=False)
print(f"Filtered PrimeKG size: {filtered_primekg.shape}")
