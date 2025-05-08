import pandas as pd
import plotly.graph_objects as go

# Load CSV
csv_path = input("Enter path to your CSV file: ")
df = pd.read_csv(csv_path)

# Show columns to help user pick
print("\nAvailable columns:", list(df.columns))

# Prompt for user
source_col = input("Enter the column name to use as the *source* (e.g. 'assayMethod'): ")
target_col = input("Enter the column name to use as the *target* (e.g. 'perturbagen'): ")
value_col = input("Enter the column name to use as the *value* (e.g. 'countOfDatasets'): ")

# All unique labels
labels = pd.concat([df[source_col], df[target_col]]).unique().tolist()

# Map labels to indices
label_map = {label: i for i, label in enumerate(labels)}

# Create lists of indices for Sankey diagram
sources = df[source_col].map(label_map).tolist()
targets = df[target_col].map(label_map).tolist()
values = df[value_col].tolist()

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    ))])

fig.update_layout(title_text="Sankey Diagram", font_size=12)
fig.show()
