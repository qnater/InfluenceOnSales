# Welcome to Influence On Sales on Amazon graphs
*This project is directed by the University of Fribourg in the context of the course FS2023: 63091 Social Media Analytics*

To be able to use the Influence on Sales application, please followed the belowed steps for installation, user guide and information.

# Installation
To install and use the Influence On Sales application, you will need :
1) First create a directory on your computer and open a terminal on this directory.
2) On the terminal, clone the GitHub repository by copying pasting this command : ```git clone https://github.com/qnater/InfluenceOnSales.git```
3) Once clone, you can open your PyCharm or python environment. On the Terminal of PyCharm or your computer, install or requirements with the command : ```pip install -r requirements.txt```
4) If an error appears, we may need to install pip.
5) Once install, the application can be run. To understand the different features and command, please follow the bellowed user guide.


# User Guide
The Influence on Sales application is able to load amazon datasets refined for the project and run different modules as Analytics, Enrichment, Exploration, Persistence, Pre-Processing and Visualization.

## project_launcher.py
The class "project_launcher.py", you can found all different scenarios prepared to express all features.

### Scenario 1 : Pre-Processing of the dataset
This scenario displays the process and the values of steps of pre-processing.

#### datasets
amazon-meta.txt (700'000), dataset_off_amazon_enrichment.txt (180'000),  dataset_off_amazon_big.txt (120'000), dataset_off_amazon_small.txt (60'000)

#### variables
XXX



### Scenario 2 : Community Detection
XXX

#### datasets
XXX

#### variables
XXX



### Scenario 3 : Visualization
XXX

#### datasets
XXX

#### variables
XXX



### Scenario 4 : Exploration
XXX

#### datasets
XXX

#### variables
XXX



### Scenario 5 : Overall run
XXX

### datasets
XXX

### variables
XXX
    
    
## z_circle_ci_unit_test.py
The file has been made to run every possible implementation in the GitHub Circle CI as unit tests.

## z_enrichment_launcher.py
This file has been implemented to test and make the merge of the current amazon graph and the enriched dataset.

## z_persistence_launcher.py
This file has been implemented to test and populate the database online Neo4J.


