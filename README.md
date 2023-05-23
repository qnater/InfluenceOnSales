# Welcome to Influence On Sales on Amazon graphs
*This project is directed by the University of Fribourg in the context of the course FS2023: 63091 Social Media Analytics*

To be able to use the Influence on Sales application, please follow the steps below for installation, user guide and information.

# Installation
To install the Influence On Sales application, you will need to:
1) First create a directory on your computer and open a terminal on this directory.
2) On the terminal, clone the GitHub repository by copying pasting this command : ```git clone https://github.com/qnater/InfluenceOnSales.git```
3) Once clone, you can open your PyCharm or python environment. On the Terminal of PyCharm or your computer, install or requirements with the command : ```pip install -r requirements.txt```
4) If an error appears, we may need to install pip.
5) Once install, the application can be run. To understand the different features and command, please follow the bellowed user guide.


# User Guide
The Influence on Sales application is able to load and refine amazon datasets, in order to run different modules such as Pre-Processing, Enrichment, Analytics, Exploration, Persistence and Visualization.

## project_launcher.py
In this class you can find five scenarios to conduct the modules.

### Scenario 1 : Pre-Processing of the dataset
In this scenario, the initial dataset will be cleaned and sampled into four different graphs. This process will be displayed by providing information on the number of nodes and quality of the clustering for each graph.

#### Used datasets
_file (number of nodes of the graph)_

amazon-meta.txt (700'000), dataset_off_amazon_enrichment.txt (180'000),  dataset_off_amazon_big.txt (120'000), dataset_off_amazon_small.txt (60'000)

#### Returned metrics
Clustering coefficient, number of nodes.



### Scenario 2 : Community Detection
In this scenario, two of the in scenario 1 generated graphs will be analysed and compared. To do so, on each graph, three different community detection algorithms are executed, 
popular nodes are identified and community partition quality is evaluated.

#### Used datasets
_file (number of nodes of the graph)_

dataset_off_amazon_enrichment.txt (180'000),  dataset_off_amazon_big.txt (120'000)

#### Returned metrics
Popular nodes of each community, silhouette index, accuracy, precision, recall, Jaccard similarity



### Scenario 3 : Visualization
In this scenario, a small sample of the initial dataset will be used to visualize the graph. After running the proper algorithms, the graph will be plotted
with communities in different colors, and the most popular node inside each highlighted.

#### Used datasets
_file (number of nodes of the graph)_

dataset_off_amazon_test.txt (11'990)

#### Returned 
Plot image



### Scenario 4 : Exploration
In this scenario, a small sample of the initial dataset will be used to conduct a deep analysis of the quality of the graph, as well as 
the connections between nodes and communities (paths).

#### Used datasets
_file (number of nodes of the graph)_

dataset_off_amazon_test.txt (11'990)

#### Returned metrics
XXX



### Scenario 5 : Overall run
This scenario consists of all four above described scenarios, which will be conducted in succession.

### Used datasets
_file (number of nodes of the graph)_

Based on the user choice between:

dataset_off_amazon_enrichment.txt (180'000),  dataset_off_amazon_big.txt (120'000), dataset_off_amazon_small.txt (60'000), dataset_off_amazon_test.txt (11'990)

### Returned metrics
XXX 
    
    
## z_circle_ci_unit_test.py
This file allows the unit tests of every possible implementation in the GitHub Circle CI.

## z_enrichment_launcher.py
This file allows the merge of the main amazon datasetg with the enriched dataset.

## z_persistence_launcher.py
This file allows the population of the database online Neo4J.


