import datetime
import json
import networkx as nx

from analytics.analytics_graph import AnalyticsGraph
from explore.exploration_graph import ExploreGraph


class EnrichmentGraph:

    def merge_for_enrichment(self, original_graph, enrichment_file="formatted_amazon_meta"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Merge a dataset of extract enriched nodes with neighbors with the original graph of amazon
        :param original_graph: Graph networkX of the dataset
        :type original_graph: networkX
        :param enrichment_file: name of the file used to merge
        :type enrichment_file: string
        :return: The merged enriched graph
        """

        current_time = datetime.datetime.now()
        print(">> You have called an enrichment of your current graph, (at", current_time, "), please wait for the merge...")

        # Create a graph
        filename = "./dataset/test_dataset/" + str(enrichment_file)
        enrichment = ExploreGraph.construct_graph_by_file(self, file_name=filename,  limit=16010574)

        merged = nx.compose(original_graph, enrichment)

        communities_merged = AnalyticsGraph.amazon_community_detection(self, graph=merged, tag="merged", run_silhouette=False, sub_function=True)
        communities_original = AnalyticsGraph.amazon_community_detection(self, graph=original_graph, tag="original_graph", run_silhouette=False, sub_function=True)

        score_merged = AnalyticsGraph.silhouette_score(self, merged, communities_merged, 'euclidean', 1000)
        score_original = AnalyticsGraph.silhouette_score(self, original_graph, communities_original, 'euclidean', 1000)

        print("\t\t (ENR) : Number of nodes added  -> ", merged.number_of_nodes()-original_graph.number_of_nodes())
        print("\t\t (ENR) : Number of edges added  -> ", merged.number_of_edges()-original_graph.number_of_edges())
        print("\t\t (ENR) : Increase of the Silhouette Index Score -> ", score_merged-score_original)

        current_time = datetime.datetime.now()
        print(">> The merge of your enrichment graph is done, (at", current_time, "), thank you...\n")

        return merged

    def compute_enrichment(self, file="meta_Books", amazon_meta="amazon-meta", new_amazon_meta="formatted_amazon_meta"):
        """
        Creator : Emmanuel Cazzato
        reviewed by : Quentin Nater
        Extract the shared ASIN from a dataset to another (get only one with shared neighbor)
        :param meta_Books: name of the json file of an enriched amazon dataset
        :type meta_Books: string
        :param amazon_meta: name of the txt file of the based amazon dataset
        :type amazon_meta: string
        :param amazon_meta: name of future dataset of the new amazon enriched file
        :type amazon_meta: string
        """

        current_time = datetime.datetime.now()
        print(">> You have search correspondence between two sets for enrichment, (at", current_time, "), please wait...")

        json_file_path = "./dataset/origin_dataset/"+file+".json"
        amazon_meta_file_path = "./dataset/origin_dataset/"+amazon_meta+".txt"
        new_amazon_meta_file_path = "./dataset/test_dataset/"+new_amazon_meta+".txt"

        # Load JSON data
        asin_with_neighbor = {}
        with open(json_file_path, 'r') as json_file:
            for line in json_file:
                data = json.loads(line)
                asin = data.get("asin")
                also_buy = data.get("also_buy", [])
                if asin:
                    asin_with_neighbor[asin] = also_buy

        print(f'\t\t\t (ENR) : Loaded {len(asin_with_neighbor)} ASINs from JSON file.')

        # Parse amazon-meta.txt and update neighbor info
        asin_similarities = {}
        with open(amazon_meta_file_path, 'r', encoding='utf-8', errors='ignore') as old_file:
            asin = None
            for line in old_file:
                line = line.strip()  # Remove leading/trailing whitespace

                # If current line defines an ASIN, remember it
                if line.startswith("ASIN:"):
                    asin = line.split(" ")[1]
                    print(f'\t\t\t\t (ENR) : ASIN {asin} from {file} has been found in in {amazon_meta} file.')
                # If current line defines similar items, and ASIN is in JSON data, update it
                elif line.startswith("similar") and asin in asin_with_neighbor:
                    similar_asins = line.split(" ")[2:]
                    asin_similarities[asin] = similar_asins
                    for neighbor in asin_with_neighbor[asin]:
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

        current_time = datetime.datetime.now()
        print(">> Finished writing formatted data ", new_amazon_meta_file_path, ", (at", current_time, ").")
