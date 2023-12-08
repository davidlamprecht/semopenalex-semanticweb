## Entity Embeddings for SemOpenAlex-SemanticWeb

### Pre-processing and Embedding training

*01:* Extracts triples from full RDF dump of SemOpenAlex-SemanticWeb, delete auxiliary classes and map all URIs to integers.  
      The pre-processing steps lead to a dataset with 2,873,866 triples, 343,192 entities (from 7 different classes) and 15
      relations.

*02:* Train TransE entity embeddings.

*03:* Train DistMult entity embeddings.  

*04:* Train ComplEx entity embeddings.

*05:* Train RotatE entity embeddings.



### Evaluation results

We spilt triples in the dataset into a training set with 80%, a validation set with 10% and
a test set with 10% of the total triples. We trained a maximum of 900 epochs
using early-stopping based on the mean rank on the validation sets, calculated every 300 epochs.
The validation mean rank for the validation set can be seen in the [validation-early-stopping](./validation-early-stopping) folder.
For DistMult training was stopped after 300 epochs. For RotatE training was stopped after 600 epochs. TransE and ComplEx
trained 900 epochs. For TransE, DistMult and RotatE the Adam Optimizer was used,
for ComplEx Adagrad. The final hyperparamters used for the training are provided in the Table below. For DistMult and ComplEx furthermore a weight decay of 1e-6 is used.

| Hyperparameter  | Value | 
|---------|-------:|
| Embedding Size      | 128 |  
| Optimizer param (Lr)  |  0.001 | 
| Batch size  |  2000 |
| Negative sampling size |  2000 |



Final evaluation results. The best values for the metrics mean rank (MR) and Hits@N are marked bold.

| Metric  | TransE | DistMult | ComplEx | RotatE |
|---------|-------:|---------:|--------:|----------:|
| MR      | **733.95** |  2047.90  |  10,626.76 |   6997.81  |
| Hits@1  |  **0.1600** |  0.0469   |  0.0309  |   0.0145   |
| Hits@3  |  **0.2458** |  0.1039   |  0.0601  |   0.0189   |
| Hits@10 |  **0.3621** |  0.2129   |  0.1177  |   0.0264  |



### Technical details
All computational tasks were carried out on the bwUniCluster 2.0 infrastructure using a node equipped with an NVIDIA A100 80GB GPU. 
All scripts for embeddings generation were conducted in an isolated virtual environment running Python 3.9.7, torch 2.0, torch-geometric 2.4 and CUDA 12.0.
