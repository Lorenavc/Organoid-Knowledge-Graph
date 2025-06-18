# ArrayExpress Metadata Column Description

The `ArrayExpress_metadata.csv` file contains curated metadata for organoid-related datasets from ArrayExpress. It consists of 18 columns, each described below

---

### Column Descriptions

**`title`** The dataset title in ArrayExpress was added to this column. The Dataset nodes’ name property was populated using the values from this column. 

**`doi`** If the publication related to the dataset was included in the ArrayExpress dataset page, the doi of that publication was added to this column. The Dataset nodes’ doi property was populated using the values from this column. 

**`publication`** If the publication related to the dataset was included in the ArrayExpress dataset ‘Publication’ section, the publication title was added to this column. The Dataset nodes’ publication property was populated using the values from this column. 

**`AE_data_type`** The terms in this column were taken from the ArrayExpress dataset ‘Study Type’ section, which uses the Experimental Factor Ontology (EFO). After examining the Description section, Protocols table, and Investigation Design Format Files (when available) on the ArrayExpress dataset page, we noticed that various datasets’ ‘Study Type’ section were not annotated with the most precise EFO terms. Thus, this column was not used to populate any node properties.

**`data_type`** This column contains the corrected ‘Study Type’ EFO term, which was assigned after examining the Description section, Protocols table, and Investigation Design Format Files (when available) on the ArrayExpress dataset page. The Assay nodes’ name property was populated using the values from this column. 

**`protocol`**  This column was used for preliminary annotations of the protocols included in the ArrayExpress datasets ‘Protocol’ section or description. An ‘x’ in this column refers to datasets that did not include information related to organoid growth protocols. An ‘sc’ was added in this column for datasets that include a sample collection protocol. These either described the collection of cells that the organoid was derived from or described organoid passaging processes. An ‘-’ was added in this column for datasets that included some information related to the main organoid growth protocol, but that information might be incomplete or not easily found in the dataset page (e.g. organoid growth protocol information would be described in the publication related to this dataset but not directly in the dataset ‘Protocol’ section). While these annotations were primarily intended for internal use, they gave us an overview of how well each dataset reported its protocols. For a more formal assessment of dataset completeness and data availability, refer to the MINSEQE Score, which evaluates adherence to the Minimum Information About a High-Throughput Nucleotide Sequencing Experiment guidelines.

**`data_location`** This column contains the ArrayExpress datasets’ website link. The Dataset nodes’ https property was populated using the values from this column. 

**`main_protocol`** This column contains the main organoid growth protocol reference in an APA citation style. The Protocol nodes’ name property was populated using the values from this column. 

**`main_protocol_doi`** This column contains the doi of the publication describing the main organoid growth protocol. 

**`other_protocol`** This column contains the additional organoid growth protocols that were cited alongside the main protocol. Typically, these additional organoid growth protocols were referenced when the main protocol was modified or supplemented with details from other published protocols. 

**`type`** This column was used for classifying the dataset as either ‘Normal’, ‘Perturbed’, or ‘Disease.’ ‘Normal’ refers to datasets of organoids that were neither perturbed nor related to disease. ‘Perturbagen’ refers to datasets of organoids that had a perturbagen applied to them. ‘Disease’ refers to datasets of organoids that were derived from diseased individuals. 

**`perturbagen`** This column contains the ontology term(s) for the perturbagen(s) applied to the organoid. The Perturbagen nodes’ name property was populated using the values from this column. 

**`perturbagen_source`** This column contains the name of the ontology or taxonomy that was used to standardize the perturbagen terms. The Perturbagen nodes’ source property was populated using the values from this column. 

**`perturbagen_id`** This column contains the term id from the ontology or taxonomy used to standardize the perturbagen term. The Perturbagen nodes’ source_id property was populated using the values from this column. 

**`organ`** This column contains the UBERON term of the organ(s) or tissue(s) the organoid data relates to. The Organoid Type nodes’ name property was populated using the values from this column. 

**`source`** This column contains the Brenda Tissue Ontology (BTO) term of the cell(s) used to grow the organoid. The Organoid Source nodes’ name property was populated using the values from this column. 

**`authors`** This column contains the name of the dataset contributors. The Dataset nodes’ contributors property was populated using the values from this column. 

**`year`** This column contains the year that the dataset was published in ArrayExpress. The Dataset nodes’ year property was populated using the values from this column.

---
