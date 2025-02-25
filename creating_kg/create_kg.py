import pandas as pd
from neomodel import db, config, StructuredNode, RelationshipTo, StringProperty, IntegerProperty
import getpass  

# Prompt the user to input their username and password
username = input("Enter your Neo4j username: ")
password = getpass.getpass("Enter your Neo4j password: ")

# Use the provided credentials to form the connection URL
config.DATABASE_URL = f"bolt://{username}:{password}@localhost:7687"

# Test the connection
try:
    db.set_connection(config.DATABASE_URL)
    db.cypher_query("RETURN 1")
    print("Connection to Neo4j established successfully!")
except Exception as e:
    print(f"Connection failed: {e}")

# Read the CSV file
df = pd.read_csv('ArrayExpress_dataset_metadata.csv')

# Filter the DataFrame to include only rows with year 2019 and later
#df = df[df['year'] >= 2019]

# Define nodes and relationships
class Assay(StructuredNode):
    name = StringProperty(unique_index=True)
    description = StringProperty()
    related_tissue = RelationshipTo('Organoid_type', 'PROFILED')
    related_dataset = RelationshipTo('Dataset', 'IS_ASSAY_METHOD_OF')

class Dataset(StructuredNode):
    name = StringProperty(unique_index=True)
    https = StringProperty()
    year = IntegerProperty()
    contributors = StringProperty()
    publication = StringProperty()
    doi = StringProperty()


    related_assay = RelationshipTo('Assay', 'HAS_ASSAY_METHOD')
    related_source = RelationshipTo('Organoid_source', 'DERIVES_FROM')
    #related_contributors = RelationshipTo('Contributors', 'CONTRIBUTOR')
    related_organoid_type = RelationshipTo('Organoid_type', 'RELATED_TO')
    related_perturbagen = RelationshipTo('Perturbagen', 'HAS_PERTURBAGEN')
    related_protocol = RelationshipTo('Protocol', 'HAS_PROTOCOL')

class Organoid_type(StructuredNode):
    name = StringProperty(unique_index=True)
    related_dataset = RelationshipTo('Dataset', 'ASSOCIATED_WITH')
    related_assay = RelationshipTo('Assay', 'PROFILED_BY')

#class Contributors(StructuredNode):
    #name = StringProperty(unique_index=True)
    #related_dataset = RelationshipTo('Dataset', 'CONTRIBUTED_TO')

class Organoid_source(StructuredNode):
    name = StringProperty(unique_index=True)
    related_dataset = RelationshipTo('Dataset', 'DERIVES_INTO')

class Perturbagen(StructuredNode):
    name = StringProperty(unique_index=True)
    term_id = StringProperty()
    standardized_knowledge_framework = StringProperty()
    related_dataset = RelationshipTo('Dataset', 'IS_PERTURBAGEN_OF')

class Protocol(StructuredNode):
    reference = StringProperty(unique_index=True)
    related_dataset = RelationshipTo('Dataset', 'HAS_PROTOCOL')

# Helper function to retrieve or create a node
def get_or_create_node(node_class, **properties):
    try:
        return node_class.nodes.get(**properties)
    except node_class.DoesNotExist:
        return node_class(**properties).save()

assay_descriptions = {
        "RNA-seq of coding RNA": "An assay in which sequencing technology (e.g. Solexa/454) is used to generate RNA sequence, from the presumed coding transcibed regions of the genome, or analyse these or to quantitate transcript abundance.",
        "RNA-seq of total RNA": "An assay in which sequencing technology (e.g. Solexa/454) is used to generate RNA sequence, from the total cellular and organelle RNA molecules isolated from a specimen, to analyse these and/or to quantitate transcript abundance.",
        "scATAC-seq": "A method for detecting the accessible chromatin in individual cells by transposase-accessible chromatin sequencing assay.",
        "RNA-seq of coding RNA from single cells": "An assay in which sequencing technology (e.g. Illumina) is used to generate RNA sequence, from the presumed coding transcibed regions of the genome, or analyse these or to quantitate transcript abundance in individual cells instead of a population of cells.",
        "transcription profiling by array": "An assay in which the transcriptome of a biological sample is analysed using array technology.",
        "RNA-seq": "RNA-seq is a method that involves purifying RNA and making cDNA, followed by high-throughput sequencing.",
        "methylation profiling by array": "An assay in which the methylation state of DNA is determined and is compared between samples using array technology",
        "CROP-Seq": "CRISPR droplet sequencing (CROP-seq)",
        "DNA-seq" : "An assay in which -sequencing technology (e.g. Solexa/454) is used to determine NDNA sequence",
        "spatial transcriptomics by high-throughput sequencing": "A spatial transcriptomics assay that measures spatially defined transcription by high-throughput sequencing.",
        "methylation profiling by high throughput sequencing": "An assay in which the methylation state of DNA is determined and is compared between samples using sequencing based technology.",
        "microRNA profiling by high throughput sequencing": "An assay in which high throughput sequencing technology is used to analyse the microRNA component of the transcriptome.",
        "single nucleus RNA sequencing": "Single nucleus RNA sequencing examines the sequence information from individual nuclei with optimized next generation sequencing (NGS) technologies. This allows the RNA-seq profiling of cell types that are more vulnerable to the tissue dissociation process, and that are therefore underrepresented in the final data set in single cell sequencing.",
        "ChIP-seq": "ChIP-seq is an assay in which chromatin immunoprecipitation with high throughput sequencing is used to identify the cistrome of DNA-associated proteins.",
        "ATAC-seq": "Assay for transposase-accessible chromatin using sequencing (ATAC-seq), is a method based on direct in vitro transposition of sequencing adaptors into native chromatin, and is a rapid and sensitive method for integrative epigenomic analysis. ATAC-seq captures open chromatin sites using a simple two-step protocol."

    # Add other assay descriptions as needed
    }
    
# Loop through the DataFrame and create nodes and relationships
for _, row in df.iterrows():
    study_title = row['title']
    https = row['data_location']
    year = row['year']
    publication = row['publication'] if pd.notna(row['publication']) else "Associated publication was not specified."
    doi = row['doi']   
    assays = [assay.strip() for assay in row.get('data_type', '').split(';')] if row.get('data_type') else []   
    organoid_types = [org.strip() for org in row.get('organ', '').split(';')] if row.get('organ') else []
    contributors = row['authors']
    organoid_sources = [source.strip() for source in row.get('source', '').split(';')] if row.get('source') else []
    perturbagens = [perturbagen.strip() for perturbagen in str(row.get('perturbagen', '')).split(';')] if pd.notna(row.get('perturbagen')) else []
    term_ids = [term_id.strip() for term_id in str(row.get('perturbagen_id', '')).split(';')] if pd.notna(row.get('perturbagen_id')) else []
    perturbagen_kf = [standardized_knowledge_framework.strip() for standardized_knowledge_framework in str(row.get('perturbagen_source', '')).split(';')] if pd.notna(row.get('perturbagen_source')) else []
    protocols = [protocol.strip() for protocol in str(row.get('main_protocol', '')).split(';') if protocol.strip() and not protocol.strip().startswith('E-')] if pd.notna(row.get('main_protocol')) else []
    
    # Create or retrieve the dataset node
    dataset = get_or_create_node(Dataset, name=study_title, https=https, year=year, contributors=contributors, publication= publication, doi=doi)

    # Create or retrieve assay nodes and connect
    for assay in assays:
        if assay:
            description = assay_descriptions.get(assay, "Description not available for this assay type.")
            assay_node = get_or_create_node(Assay, name=assay)
        
        # Update the description if necessary
        if not assay_node.description or assay_node.description == "Description not available for this assay type.":
            assay_node.description = description
            assay_node.save()  # Save changes to the database

        # Create relationships
        if not dataset.related_assay.is_connected(assay_node):
            dataset.related_assay.connect(assay_node)
     

    # Create or retrieve organoid source nodes and connect
    for source in organoid_sources:
        if source:
            source_node = get_or_create_node(Organoid_source, name=source)
            if not dataset.related_source.is_connected(source_node):
                dataset.related_source.connect(source_node)

          
    # Create or retrieve organoid type nodes and connect
    for organoid_type in organoid_types:
        if organoid_type:
            organoid_node = get_or_create_node(Organoid_type, name=organoid_type)
            if not dataset.related_organoid_type.is_connected(organoid_node):
                dataset.related_organoid_type.connect(organoid_node)

    # Create or retrieve perturbagen nodes and connect                   
    for perturbagen, term_id, standardized_knowledge_framework in zip(perturbagens, term_ids, perturbagen_kf):
        if perturbagen:
            perturbagen_node = get_or_create_node(Perturbagen, name=perturbagen, term_id=term_id)
            if standardized_knowledge_framework:
                perturbagen_node.standardized_knowledge_framework = standardized_knowledge_framework
            perturbagen_node.save()  
    
            if not dataset.related_perturbagen.is_connected(perturbagen_node):
                dataset.related_perturbagen.connect(perturbagen_node)


    # Create or retrieve protocol nodes and connect          
    for protocol in protocols:
        if protocol:
            protocol_node = get_or_create_node(Protocol, reference=protocol)
            if not dataset.related_protocol.is_connected(protocol_node):
                dataset.related_protocol.connect(protocol_node)


# Verify the nodes and relationships
for dataset in Dataset.nodes.all():
    print(f"Dataset: {dataset.name}")
    for assay in dataset.related_assay:
        print(f"   Related Assay: {assay.name}")
    for source in dataset.related_source:
        print(f"   Related Source: {source.name}")
    for organoid_type in dataset.related_organoid_type:
        print(f"   Related Organoid Type: {organoid_type.name}")
    for perturbagen in dataset.related_perturbagen: 
        print(f"   Related Perturbagen: {perturbagen.name}")
    for protocol in dataset.related_protocol:
        print(f"   Related Protocol: {protocol.reference}")
