import datetime
import re

import scipy

from analytics.analytics_graph import AnalyticsGraph
from explore.exploration_graph import ExploreGraph


class StatisticsGraph:
    def ranking_sales(self, txt_file="amazon-meta.txt"):
        """
        Creator: Sophie Caroni & Emmanuel Cazzato
        Reviewed by: Quentin Nater
        Retrieve ranking level of sales of the amazon products from the raw file
        :param txt_file: Amazon meta dataset
        :type txt_file: file
        :return: Dictionary for salesranks (values) of ASINs (keys)
        """
        with open("./dataset/origin_dataset/" + txt_file, "r", encoding="utf-8") as file:

            # Initialize a dictionary to later store asins and their salesranks
            salesranks = {}

            # Initialize variables to keep track of the conditions
            current_asin = None
            current_salesrank = None
            discontinued_product = False

            for line in file:

                # Strip any leading or trailing whitespace from the line
                line = line.strip()

                # Retrieve for each product its ASIN
                if line.startswith('ASIN:'):
                    asin = line.split()[1]
                    current_asin = ExploreGraph.convert_asin_to_int(self, asin)

                # Check if product is labelled as discontinued (so no salesrank)
                if line.startswith('  discontinued product'):
                    discontinued_product = True

                # Retrieve for each product its salesrank
                if line.startswith('salesrank:') and not discontinued_product:
                    current_salesrank = line.split()[1]
                    # Do not include products having 0 as ralesrank
                    if current_salesrank == '0':
                        current_salesrank = None

                # Add to the dictionary ASIN (key) and salesrank (value)
                if current_asin is not None and current_salesrank is not None:
                    salesranks[current_asin] = int(current_salesrank)
                    current_asin = None
                    current_salesrank = None
                    discontinued_product = False

        return salesranks

    def real_popularities(self, graph, community_output_file):
        """
        Creator: Sophie Caroni
        Reviewed by: Quentin Nater
        Compute popularity scores relative to the whole graph of community-popular products
        :param graph: Graph networkX of the dataset
        :type graph: networkX
        :param community_output_file: Ouptut of the community detection algorithm
        :type community_output_file: .txt file
        :return: Dictionary for popularity scores (values) of ASINs (keys)
        """
        current_time_start = datetime.datetime.now()
        print("\n>> You have called the computing of popularity scores (relative to the entire graph) of community-popular nodes (at", current_time_start, ").")

        # Initialize the dictionary to store the popularity scores from the community detection
        comm_popularity_scores = {}

        # Initialize the dictionary to store the final popularity scores
        real_popularity_scores = {}

        # Read the community detection output file
        with open("./results/scenario_5/" + community_output_file, "r", encoding="utf-8") as file:
            content = file.read()

            # Retrieve the popular nodes of each community
            pattern = r"\[(\d+(\.\d+)?), (\d+)\]"
            matches = re.findall(pattern, content)

            # Store for each product its ASIN and popularity score
            for match in matches:
                score = match[0]
                asin = match[2]
                comm_popularity_scores[asin] = score

        # Calculate the popularity scores relative to the entire graph
        graph_popularity_scores = AnalyticsGraph.betweenness_centrality_scores(self, graph=graph)

        # Add to the final dictionary ASIN (key) and this updated popularity score (value)
        for asin in comm_popularity_scores.keys():
            real_popularity_scores[int(asin)] = graph_popularity_scores[int(asin)]

        current_time_end = datetime.datetime.now()
        print(">> The computing of popularity scores relative to the entire graph as finished (at", current_time_end, ", taking ", current_time_end - current_time_start, "minutes).")

        return real_popularity_scores

    def correlate_popularity_and_sales(self, products_popularity_scores, products_salesranks):
        """
        Creator: Sophie Caroni
        Reviewed by: Quentin Nater
        Compute correlation between popularity score and salesrank of community-popular products
        :param products_popularity_scores: Popularity scores (relative to the whole graph) of community-popular products
        :type  products_popularity_scores: dict
        :param products_salesranks: Salesranks of all products
        :type products_salesranks: dict
        :return:
        """
        current_time_start = datetime.datetime.now()
        print(">> You have called the correlation between popularity score and salesrank (at", current_time_start, ").")

        # Initialize needed structures
        products, popularity_scores_lst, salesrank_lst = {}, [], []

        # Store in common_asins products both having a salesrank and being community-popular
        popular_asins = set(products_popularity_scores.keys())
        salesranked_asins = set(products_salesranks.keys())
        common_asins = popular_asins.intersection(salesranked_asins)

        # For those products,
        for product in common_asins:
            # store salesranks in a list
            salesrank = products_salesranks[product]
            salesrank_lst.append(salesrank)
            # store popularity score in a list
            popularity_score = products_popularity_scores[product]
            popularity_scores_lst.append(popularity_score)
            # store in a dict each ASIN as key, and salesrank with popularity score as value
            popularity_salesrank = [salesrank, popularity_score]
            products[product] = popularity_salesrank

        # Compute crrelation between salesrank and popularity score overall
        overall_corr, overall_p_value = scipy.stats.spearmanr(popularity_scores_lst, salesrank_lst)

        # Compute crrelation between salesrank and popularity score for the 15 most popular products
        sorted_popularities = sorted(popularity_scores_lst, reverse=True)[0:15]
        sorted_salesrank = []
        best_asins = []

        for asin, [salesrank, popularity] in products.items():
            if popularity in sorted_popularities:
                sorted_salesrank.append(salesrank)
                best_asins.append(asin)

        best_corr, best_p_value = scipy.stats.spearmanr(sorted_popularities, sorted_salesrank)

        print(f"\n\t\t (STAT) : correlation (& p-value) overall: {overall_corr, overall_p_value}")
        print(f"\t\t (STAT) : correlation (& p-value) of the 15 best: {best_corr, best_p_value}")

        print(f"\n\n\t\t (STAT) : popularities & salesranks of the 15 best:")
        for i in range(len(best_asins)):
            print(f"\t\t\t\t (STAT) : asin: {best_asins[i]}")
            print(f"\t\t\t\t\t\t (STAT) : score = {sorted_popularities[i]}")
            print(f"\t\t\t\t\t\t (STAT) : salesrank = {sorted_salesrank[i]}")


        current_time_end = datetime.datetime.now()
        print(">> The compute of correlations between popularity scores and salesranks has finshed (at",
              current_time_end, ", taking ", current_time_end - current_time_start, "minutes).")

