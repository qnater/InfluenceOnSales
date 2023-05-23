import datetime


class ExportGraph:

    def create_dataset(self, graph, name):
        """
        Creator : Sophie Caroni
        reviewed by : Quentin Nater
        Create a .txt dataset with the for our analysis meaningful information only
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :param name: string - name inside the dataset file
        :type name: string
        :return: -
        """

        current_time = datetime.datetime.now()
        print("\n>> You have called the export of your graph, (at", current_time, "), please wait...")

        # Create new .txt file
        with open("./dataset/" + str(name) + ".txt", "w", encoding="utf-8") as file:

            # Retrieve ASIN from node
            asin_lst = graph.nodes()

            # For every ASIN, retrieve its similars
            for asin in asin_lst:
                sim_lst = []
                for adj in graph.edges():
                    if asin == adj[0]:
                        sim_lst.append(adj[1])

                # Define the entries of the file for ASIN having similars
                if len(sim_lst) != 0:
                    entries = ["ASIN: " + str(asin),
                               "  similar: " + str(len(sim_lst)) + "  " + "  ".join(str(i) for i in sim_lst)]

                # Define the entries of the file for ASIN not having similars
                elif len(sim_lst) == 0:
                    entries = ["ASIN: " + str(asin), "  similar: " + str(len(sim_lst))]

                # Write the file sticking to the correct (original) nomenclature
                for entry in entries:
                    file.write(entry)
                    file.write('\n')
                file.write('\n')

        current_time = datetime.datetime.now()
        print(">> Job done, the refined graph in this directory './dataset/', (at", current_time, "), thank you...")

        return

    def export_communities_results(self, run_time, communities, popular, acc, pre, rec, jac, silhouette, tag="default", scenario="2"):
        """
        Creator : Quentin Nater
        reviewed by : Quentin Nater
        Save the data from the scenario on a file
        :param run_time: float - Run time of the community detection
        :type run_time: float
        :param communities: list of string - List of community detection by the algorithm
        :type communities: list of string
        :param popular: list of string - List of popular nodes of each community
        :type popular: list of string
        :param acc: float - Accuracy of the community algorithm
        :type acc: float
        :param pre: float - Precision of the community algorithm
        :type pre: float
        :param pre: float - Precision of the community algorithm
        :type pre: float
        :param rec: float - Recall of the community algorithm
        :type rec: float
        :param jac: float - Jaccard similitude value of the community algorithm
        :type jac: float
        :param silhouette: float - Silhouette Index of the communities
        :type silhouette: float
        :param tag: string - Name of the output file of results
        :type tag: string
        :param scenario: string - Number of scenario played
        :type scenario: string
        :return: -
        """

        with open("./results/scenario_"+str(scenario)+"/" + str(tag) + ".txt", 'w') as file:
            file.write("Results of the community detection of " + str(tag) +
                       "\nRun Time : " + str(run_time) +
                       "\nSilhouette Index : " + str(silhouette) +
                       "\nAccuracy : " + str(acc) +
                       "\nPrecision : " + str(pre) +
                       "\nRecall : " + str(rec) +
                       "\nJaccard : " + str(jac) +
                       "\nNumber of communities : " + str(len(communities)) +
                       "\nCommunities : " + str(communities) +
                       "\nPopular : " + str(popular))

