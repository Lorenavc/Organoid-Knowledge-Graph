# Organoid-Knowledge-Graph

Organoid Knowledge Graph (Organoid KG) was created in the neo4j database and emcompasses 147 human organoid multiomics datasets from Array Express; it includes nodes such as organoid type, source of organoid, assay method, perturbagen applied, and main organoid growth protocol(s) used. Additionally, we integrated our organoid knowledge graph with PrimeKG, a biomedical knowledge graph, to make the combined resource more comprehensive and to showcase the versatility of a graph structure. 

![Alt text](images/Organoid KG example nodes.png)

## Organoid KG Metadata 

  | Metadata       | Definition      | Ontology or Knowledge Database used for Standardization       |
|------------------|--------------------|-------------------------------|
| Organoid Type         | the specific organ or tissue that the organoid represents or is derived from   | UBERON |
| Assay Method | the experimental techniques used to measure and analyze biological molecules at a large scale, such as RNA-seq, DNA-seq, ATAC-seq, etc        | Experimental Factor Ontology (EFO) |
| Organoid Source      | the type of cells utilized to grow the organoid  | Brenda Tissue Ontology (BTO) |
| Perturbagen | any drugs, genetic modifications, infections, or other treatments that were applied to the organoid | BioAssay Ontology (BAO), National Center for Biotech Institute Thesaurus (NCIT), Ontology of Genes and Genomes (OGG), Systematized Nomenclature of Medicine Clinical Terms (SNOMED), PRotein Ontology (PR), Ontology for MicroRNA Target (OMIT)  |
| Protocol | the main growth protocol used to create the organoid | Protocol Reference used | 

## Environment Setup

## Building Organoid KG

## Integrating Organoid KG with PrimeKG 

## Supplementary Material



