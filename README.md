# Organoid-Knowledge-Graph

Organoid Knowledge Graph (Organoid KG) was created in the neo4j database and emcompasses 147 human organoid multiomics datasets from Array Express; it includes nodes such as organoid type, source of organoid, assay method, perturbagen applied, and main organoid growth protocol(s) used. Additionally, we integrated our organoid knowledge graph with PrimeKG, a biomedical knowledge graph, to make the combined resource more comprehensive and to showcase the versatility of a graph structure. 

![Alt text](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/images/organoidKG_example_diagram.png)

## Organoid KG Metadata 

  | Metadata       | Definition      | Ontology or Knowledge Database used for Standardization       |
|------------------|--------------------|-------------------------------|
| Organoid Type         | the specific organ or tissue that the organoid represents or is derived from   | UBERON |
| Assay Method | the experimental techniques used to measure and analyze biological molecules at a large scale, such as RNA-seq, DNA-seq, ATAC-seq, etc        | Experimental Factor Ontology (EFO) |
| Organoid Source      | the type of cells utilized to grow the organoid  | Brenda Tissue Ontology (BTO) |
| Perturbagen | any drugs, genetic modifications, infections, or other treatments that were applied to the organoid | BioAssay Ontology (BAO), National Center for Biotech Institute Thesaurus (NCIT), Ontology of Genes and Genomes (OGG), Systematized Nomenclature of Medicine Clinical Terms (SNOMED), PRotein Ontology (PR), Ontology for MicroRNA Target (OMIT), DrugBank  |
| Protocol | the main growth protocol used to create the organoid | Protocol Reference used | 

## 🌱 Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Lorenavc/Organoid-Knowledge-Graph.git
cd Organoid-Knowledge-Graph
```

### 2. Install Dependencies


```bash
pip install -r requirements.txt
```

### 3. Start Neo4j (using Docker)

```bash
docker run -d --name neo4j-instance -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/yourpassword -v /creating_kg/ArrayExpress_metadata.csv:/data/ArrayExpress_metadata.csv neo4j:latest
```

## 🧑‍💻 Creating Organoid KG

### 4. Running the Script

When you run the script [create_kg.py](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/creating_kg/create_kg.py), you’ll be prompted to enter your Neo4j username and password:

bash  
Enter your Neo4j username: neo4j  
Enter your Neo4j password: yourpassword

After inputting your username and password, open the http://localhost:7474 in your browser to access the Neo4j Browser interface.

### 5. Visualizing KG
You can run the following Cypher query to visualize the entire graph:

```cypher
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

## 🧩 Integrating Organoid KG with PrimeKG 

### 6. Filter PrimeKG csv
Prior to integration, we examined the PrimeKG csv file, which includes columns used to define edges, nodes, and node properties. Organoid KG dataset nodes have a name property, so we used Bash grep commands to search for Organoid KG node names within the PrimeKG csv file. We found matches corresponding to the ‘organoid type’ and ‘perturbagen’ node types. Thus, to save computational time, the [filter_primekg.py](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/integrating_kg/filter_primekg.py) script uses node names corresponding to the ‘organoid type’ and ‘perturbagen’ node types to filter the original PrimeKG csv. The resulting file is [uni_filt_primekg.csv](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/integrating_kg/uni_filt_primekg.csv). The script also provides comments to guide you if filtering a csv other than PrimeKG's. 

### 7. Integrate Organoid KG and PrimeKG in Neo4j 

The script [integrate.py](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/integrating_kg/integrate.py) connects to a Neo4j database containing the Organoid KG, reads the filtered PrimeKG csv, and constructs a Cypher query that merges nodes based on their node names, sets node properties and classes, and creates relationships between nodes.


## 📄 Supplementary Scripts

The script [GEO_ID_download.py](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/supplementary_scripts/GEO_ID_download.py) was created to extract GEO (Gene Expression Omnibus) accession IDs from the NCBI database based on a specific search query ('(((organoid[Description]) AND Homo sapiens[Organism]) AND ("2019"[Publication Date] : "3000"[Publication Date])) NOT cancer') and save them to a .txt file as a comma-separated list.

These IDs extracted and saved by the GEO_ID_download.py script were used in the R script [GEO_file_download.R](https://github.com/Lorenavc/Organoid-Knowledge-Graph/blob/main/supplementary_scripts/GEO_file_download.R) to download GEO dataset supplementary files, which often contain raw count data.

