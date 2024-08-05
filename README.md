Traditional Chinese Medicine prescription generation model (TCMP_Gen) 
This project implements a system for analyzing Traditional Chinese Medicine (TCM) prescriptions using association rules and graph clustering techniques. It provides a graphical user interface for inputting parameters, processing data, and visualizing results.

Features

Data processing and association rule mining using the Apriori algorithm
Graph clustering and visualization of TCM formula relationships
Interactive GUI for parameter input and result display
Generation of network graphs and subgraphs based on association rules

Requirements

Python 3.9
Required libraries:

matplotlib==3.7.0
networkx==3.0
numpy==1.24.2
pandas==1.5.3
pypinyin==0.48.0
Requests==2.32.0



File Structure

main.py: Entry point of the application
Rule/apriori.py: Implementation of the Apriori algorithm and GUI
Rule/utils.py: Utility functions for data processing and association rule mining
graphclustering/graphdraw.py: Functions for graph creation and visualization
graphclustering/clustering.py: Implementation of graph clustering algorithms

Usage

Run  to start the application.main.py
In the GUI, set the minimum support and confidence values.
Select a CSV file containing TCM prescription data when prompted.
The application will process the data and generate association rules.
Results will be displayed in the GUI and saved as CSV files in the  directory.data/out/
Network graphs will be generated and saved in the  directory.graph/

Output

data/out/frequent_itemsets.csv: Contains frequent itemsets found in the data
data/out/association_rules.csv: Contains generated association rules
graph/non-directional_fully_connected_network_graph.png: Full network graph of TCM prescription relationships
graph/subgraph_X.png: Subgraphs showing clusters of closely related TCM prescriptions
