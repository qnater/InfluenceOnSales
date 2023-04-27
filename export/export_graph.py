import networkx as nx
from explore.exploration_graph import ExploreGraph as eg
import csv


class ExportGraph:

    def create_dataset(graph):
        """
        Creator : Sophie Caroni
        reviewed by :
        Create a .txt dataset with the for our analysis meaningful information only
        :param graph: networkX - Graph networkX of the amazon dataset
        :type graph: networkX
        :return: -
        """

        print(">> You have called the export of your graph, please wait :)")

        # Create new .txt file
        with open("./dataset/amazon_refined.txt", "w", encoding="utf-8") as file:

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
                    entries = ["ASIN: "+str(asin), "  similar: " + str(len(sim_lst)) + "  " + "  ".join(str(i) for i in sim_lst)]

                # Define the entries of the file for ASIN not having similars
                elif len(sim_lst) == 0:
                    entries = ["ASIN: " + str(asin), "  similar: " + str(len(sim_lst))]

                # Write the file sticking to the correct (original) nomenclature
                for entry in entries:
                    file.write(entry)
                    file.write('\n')
                file.write('\n')

        print(">> You can find your refined graph in this directory './dataset/', please enjoy ;)")

        return

    def txt_to_csv(input_file, output_file):
        """
        Creator : Sophie Caroni
        reviewed by :
        Create a .csv file of the txt amazon_refined dataset
        :param input_file: file of the amazon_refined dataset
        :type input_file: .txt
        :return: -
        """

        print(">> You have called the conversion in csv of your dataset, please wait :)")

        # Open the input txt file for reading and the output csv file for writing
        with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:

            # Create a csv writer object and write the header row to the csv file
            writer = csv.writer(csv_file)
            writer.writerow(['ASIN', 'SIMILAR_TO'])

            # Initialize a variable to keep track of the current ASIN being processed
            current_asin = None

            # Loop through each line in the input txt file
            for line in txt_file:

                # Strip any leading or trailing whitespace from the line
                line = line.strip()

                # If the line starts with 'ASIN:', extract the ASIN and set it as the current ASIN
                if line.startswith('ASIN:'):
                    current_asin = line.split()[1]

                # If the line starts with 'similar:', extract the similar ASINs and write them to the csv file
                elif line.startswith('similar:'):

                    # Extract the similar ASINs (by skipping the two first elements, i.e. "similar:" and nr of similars)
                    similar_asins = line.split()[2:]

                    # Write the current ASIN and the list of similar ASINs to the csv file
                    writer.writerow([current_asin, *similar_asins])

        return

