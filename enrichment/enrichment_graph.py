import json
import networkx as nx
from networkx.algorithms.community import louvain_communities
import networkx as nx
import random
import re
import datetime

from analytics.analytics_graph import AnalyticsGraph
from explore.exploration_graph import ExploreGraph
from preprocessing.pre_processing_graph import PreProcessGraph


class EnrichmentGraph:


    def merge_for_enchirment(self, original_graph, enchriment_file="formatted_amazon_meta"):
        # Create a graph
        filename = "./dataset/test_dataset/" + str(enchriment_file)
        enrichment = ExploreGraph.construct_graph_by_file(self, file_name=filename,  limit=16010574)

        merged = nx.compose(original_graph, enrichment)

        communities_merged = AnalyticsGraph.amazon_community_detection(graph=merged, tag="merged", run_silhouette=False)
        communities_original = AnalyticsGraph.amazon_community_detection(graph=original_graph, tag="original_graph", run_silhouette=False)

        score_merged = AnalyticsGraph.silhouette_score(merged, communities_merged, 'euclidean', 1000)
        score_original = AnalyticsGraph.silhouette_score(original_graph, communities_original, 'euclidean', 1000)

        print("Number of nodes added : ", merged.number_of_nodes()-original_graph.number_of_nodes())
        print("Number of edges added : ", merged.number_of_edges()-original_graph.number_of_edges())

        print("Difference score index : ", score_merged-score_original)

        return merged


    def compute_enrichment(self, file="meta_Books", amazon_meta="amazon-meta", new_amazon_meta="formatted_amazon_meta"):
        json_file_path = "./dataset/json/"+file+".json"
        amazon_meta_file_path = "./dataset/origin_dataset/"+amazon_meta+".txt"
        new_amazon_meta_file_path = "./dataset/test_dataset/"+new_amazon_meta+".txt"

        # Load JSON data
        json_asins_and_neighbors = {}
        with open(json_file_path, 'r') as json_file:
            for line in json_file:
                data = json.loads(line)
                asin = data.get("asin")
                also_buy = data.get("also_buy", [])
                if asin:
                    json_asins_and_neighbors[asin] = also_buy

        print(f'Loaded {len(json_asins_and_neighbors)} ASINs from JSON file.')

        # Parse amazon-meta.txt and update neighbor info
        asin_similarities = {}
        with open(amazon_meta_file_path, 'r', encoding='utf-8', errors='ignore') as old_file:
            asin = None
            for line in old_file:
                line = line.strip()  # Remove leading/trailing whitespace

                # If current line defines an ASIN, remember it
                if line.startswith("ASIN:"):
                    asin = line.split(" ")[1]
                    print(f'ASIN {asin} from {file} has been found in in {amazon_meta} file.')
                # If current line defines similar items, and ASIN is in JSON data, update it
                elif line.startswith("similar") and asin in json_asins_and_neighbors:
                    similar_asins = line.split(" ")[2:]
                    asin_similarities[asin] = similar_asins
                    for neighbor in json_asins_and_neighbors[asin]:
                        if neighbor not in similar_asins:
                            similar_asins.append(neighbor)
                    asin_similarities[asin] = similar_asins

        # Write formatted output to the new file
        with open(new_amazon_meta_file_path, 'w') as new_file:
            for asin, neighbors in asin_similarities.items():
                new_file.write(f'ASIN: {asin}\n')
                new_file.write(f'  similar: {len(neighbors)} ')
                new_file.write(' '.join(neighbors))
                new_file.write('\n')

        print(f'Finished writing formatted data to the new file {new_amazon_meta_file_path}.')

