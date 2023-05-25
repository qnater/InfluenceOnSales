# Welcome to Influence On Sales application
*This project is directed by the University of Fribourg in the context of the course FS2023: 63091 Social Media Analytics*

In order to use the Influence on Sales application, please follow the steps below for installation, user guide and information.

<br><br>

# Installation
To install the Influence On Sales application, you will need to:
1) First create a directory on your computer and open a terminal on this directory.
2) On the terminal, clone the GitHub repository. To do so, copy and paste this command : ```git clone https://github.com/qnater/InfluenceOnSales.git```
3) Once clone enter inside the clone directory with the command : ```cd InfluenceOnSales```
4) Install the requirements with the command : ```pip install -r requirements.txt```
5) If an error appears, you may need to install pip.
6) Once installed, the application can be run with one of the following commands, according to your operating system: ```python project_launcher.py``` for Windows, ```python3 project_launcher.py``` for Mac
7) To understand how to use the different features and commands, please follow the user guide below.

<br><br>

# User Guide
The Influence on Sales application enables the analysis of datasets of Amazon products, that are registered with the Amazon Standard Identification Number (ASIN). The app consists of different modules: Pre-Processing, Enrichment, Analytics, Exploration, Persistence and Visualization. These modules are integrated into the scenarios described below.
<br>
To call a scenario, simply run the *project_launcher.py* file on a terminal and write the scenario to launch on the console.


## project_launcher.py
In this class you can find six scenarios to conduct the analysis modules.

<br>

### Scenario 1 : Pre-Processing of the dataset
In this scenario, the initial dataset will be cleaned and sampled into four different graphs. This process will be displayed by providing information on the number of nodes and quality of the clustering for each graph. During the cleaning operation, we will remove unnecessary nodes (not out-edged, not in-edged and isolated). 

#### Datasets
amazon-meta.txt (700'000 nodes), dataset_off_amazon_enrichment.txt (180'000 nodes),  dataset_off_amazon_big.txt (120'000 nodes), dataset_off_amazon_small.txt (60'000)

#### Returned metrics
Runtime, Clustering Coefficient, number of nodes, number of edges, average degree.

<br><br>

### Scenario 2 : Community Detection
In this scenario, we compare algorithms of community detection with different datasets. To do so, on each graph, three different community detection algorithms are executed (simple homemade, enhanced homemade with weight and networkX library), popular nodes are identified and community partition quality is evaluated with metrics such as Accuracy, Precision, Recall, Jaccard Similarity, Silhouette Index.

#### Datasets
dataset_off_amazon_enrichment.txt (180'000 nodes),  dataset_off_amazon_big.txt (120'000 nodes)

#### Returned metrics
Runtime, silhouette index, accuracy, precision, recall, Jaccard similarity, communities detected, popular nodes of each community with centrality value.

<br><br>

### Scenario 3 : Visualization
In this scenario, a small sample of the dataset will be used to visualize the graph. After running the community detection algorithm, the graph will be plotted with communities in different colors, and the most popular node inside each highlighted.

#### Datasets
dataset_off_amazon_test.txt (11'000 nodes)

#### Returned object 
Plot image

<br>

### Scenario 4 : Exploration
In this scenario, a small sample of the initial dataset will be used to conduct a deep analysis of the quality of the graph, as well as the connections between nodes and communities (paths).

#### Datasets
dataset_off_amazon_test.txt (11'000 nodes)

#### Returned object
Plot image

<br>

### Scenario 5 : Statistical Analysis
This scenario consists of analysing the report between the betweeness centrality of the popular nodes of each community and their actual sale ranks.  

#### Datasets

dataset_off_amazon_enrichment.txt (180'000 nodes), dataset_off_amazon_test.txt (11'000 nodes)

#### Returned objects
ASIN, betweeness centrality value, sale rank 

<br>

### Scenario 6 : Overall run
This scenario consists of all four above described scenarios, which will be conducted in succession.

#### Datasets
Based on the user choice:
dataset_off_amazon_enrichment.txt (180'000 nodes), dataset_off_amazon_big.txt (120'000 nodes), dataset_off_amazon_small.txt (60'000 nodes), dataset_off_amazon_test.txt (11'000 nodes)

#### Returned objects
Runtime, Clustering Coefficient, number of nodes, number of edges, average degree, silhouette index, accuracy, precision, recall, Jaccard similarity, community detected, popular nodes of each community with centrality measures, plot images.

<br>
    
## z_circle_ci_unit_test.py
This file allows the unit tests of every possible implementation in the GitHub Circle CI.

<br>

## z_compare_algo_launcher.py
This file compares the different algorithms for group-based community detection.

<br>

## z_enrichment_launcher.py
This file allows the merge of the main amazon dataset with the enriched dataset.

<br>

## z_persistence_launcher.py & Neo4J DB
This file allows the population of the online database Neo4J.

1) You can find the database on this link : https://workspace-preview.neo4j.io/workspace/query 

2) To connect, please go to "*Query*", click on the central button "*No connection*", then on "*Connect*".
    <table>
        <tr>
            <td>Connection URL</td>
            <td>95147e5a.databases.neo4j.io:7687</td>
        </tr>
        <tr>
            <td>Database user</td>
            <td>neo4j</td>
        </tr>
        <tr>
            <td>Password</td>
            <td>GslPkJDwnmAZC_COZUcHQ1hFymVSQTzS_f6loACAyNY</td>
        </tr>
    </table>

3) To import the queries, please go on "*Saved Cypher*" and import the file "*./docs/neo4j_queries.csv*" of the project tree.

<br><br>
