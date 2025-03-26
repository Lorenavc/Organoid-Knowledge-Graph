from neo4j import GraphDatabase
import pandas as pd
import getpass

# User credentials
URI = "bolt://localhost:8788"  # Adjust if needed
USERNAME = input("Enter Neo4j username: ")
PASSWORD = getpass.getpass("Enter Neo4j password: ")

# Load the CSV
csv_file = "uni_filt_primekg.csv"  # Ensure the path is correct
df = pd.read_csv(csv_file)

# Function to insert data into Neo4j
def insert_data(tx, x_name, x_id, x_type, x_source, y_name, y_id, y_type, y_source, relation, display_relation):
    # Normalize labels and relationships
    x_type = x_type.replace('/', '_').capitalize()
    y_type = y_type.replace('/', '_').capitalize()
    relation = relation.replace(' ', '_').replace('-', '_')

    query = f"""
    MERGE (x {{name: $x_name}})
    ON CREATE SET x.id = $x_id, x.type = $x_type, x.source = $x_source
    ON MATCH SET x.id = $x_id, x.type = $x_type, x.source = $x_source
    SET x:{x_type}  

    MERGE (y {{name: $y_name}})
    ON CREATE SET y.id = $y_id, y.type = $y_type, y.source = $y_source
    ON MATCH SET y.id = $y_id, y.type = $y_type, y.source = $y_source
    SET y:{y_type}  

    WITH x, y
    MATCH (existing {{name: $x_name}})
    REMOVE existing.source_id
    MERGE (x)-[r:{relation} {{display: $display_relation}}]->(y)
    """
    tx.run(query, x_name=x_name, x_id=x_id, x_type=x_type, x_source=x_source,
                 y_name=y_name, y_id=y_id, y_type=y_type, y_source=y_source,
                 display_relation=display_relation)

# Connect to Neo4j and execute
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(insert_data, 
                              row["x_name"], row["x_id"], row["x_type"], row["x_source"], 
                              row["y_name"], row["y_id"], row["y_type"], row["y_source"], 
                              row["relation"], row["display_relation"])

driver.close()
print("✅ Data import complete!")
