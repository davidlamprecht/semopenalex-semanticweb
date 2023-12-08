## Entity Embeddings for SemOpenAlex-SemanticWeb

### Pre-processing and Embedding training

*01:* Extracts triples from full RDF dump of SemOpenAlex-SemanticWeb, delete auxiliary classes and map all URIs to integers.  
      The pre-processing steps lead to a dataset with 2,873,866 triples, 343,192 entities (from 7 different classes) and 15
      relations.

*02:* Train TransE entity embeddings.

*03:* Train DistMult entity embeddings.  

*04:* Train ComplEx entity embeddings.

*05:* Train RotatE entity embeddings.


### Technical details
All computational tasks were carried out on the bwUniCluster 2.0 infrastructure using a node equipped with an NVIDIA A100 80GB GPU. 
All scripts for embeddings generation were conducted in an isolated virtual environment running Python 3.9.7, torch 2.0, torch-geometric 2.4 and CUDA 12.0.
