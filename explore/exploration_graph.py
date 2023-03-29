import networkx as nx
import re


class ExploreGraph:

    # Creator : Quentin Nater
    # reviewed by : Sophie Caroni
    #
    # asin : string - ID of the node
    #
    # Convert the id (ASIN) into a INT unique value
    def convert_asin_to_int(asin):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if any(char.isalpha() for char in asin): # isalpha() returns True if it detects letters
            for char in asin:
                if char.isalpha():
                    asin = asin.replace(char, str(alphabet.index(char.upper()) + 10))

        return int(asin)

    # Creator : Quentin Nater
    # reviewed by : Sophie Caroni
    #
    # filename      : string - path to the dataset
    # limit         : int - limit of the line to read (sample)
    # display       : bool - display the results of the analysis
    # displayDetail : bool - display the detail of the construction
    #
    # Construct a complex graph with a file
    def construct_graph_by_file(file_name, limit=15010574, display=True, displayDetail=False):
        print(">> You have called the construction of your graph, please wait :)")

        # initialization of the variables
        graph = nx.DiGraph()
        i, asin_int, notOutEdged = 0, 0, 0
        list_asin, list_similars, list_not_out_edged, list_not_in_edged, list_extern = [], [], [], [], []

        # read every information of the file (dataset)
        with open(file_name, "r", encoding='utf-8') as f:
            for line in f:

                i += 1  # inc break

                # read nodes ===============================================
                match = re.search(r'ASIN:\s*(\w+)', line)  # each ASIN
                if match:
                    asin = match.group(1)  # Take the first element matched

                    # add a node to the graph for the ASIN value (INT)
                    asin_int = ExploreGraph.convert_asin_to_int(asin)
                    graph.add_node(asin_int)
                    list_asin.append(asin_int)

                # read edges ===============================================
                match = re.search(r'similar:\s*(\w+)', line)  # each similar
                if match:
                    similars = line.split(sep="  ") # Create a list of each one of the similars as an element
                    inc = 0

                    for similar in similars:
                        inc += 1

                        if inc > 2:  # if more than 0 categories ## ??? categories? why inc > 2? and why 0 and not 2?
                            similar_int = ExploreGraph.convert_asin_to_int(similar)  # casting
                            list_similars.append(similar_int)
                            graph.add_edge(*(asin_int, similar_int)) # Add edges between the asin product and each of its similar ones

                            if displayDetail:
                                print("\t\t\t\t(" + str(asin_int) + ", " + str(similar_int) + ")")

                        elif len(similars) == 2:  # information if it has 0 category (CHECK FOR ANALYSIS)
                            notOutEdged += 0.5  # because read 2 times
                            if notOutEdged % 1 == 0:
                                asin_i = ExploreGraph.convert_asin_to_int(asin)  # casting
                                list_not_out_edged.append(asin_i)

                # Stop reading file when the given line limit is reached =======================================
                if i == limit:
                    break

        nNodes, nEdges = graph.number_of_nodes(), graph.number_of_edges()
        print("\t\tThe graph has been successfully constructed! (nodes:" + str(nNodes) + ", edges:" + str(nEdges) + ")")

        if display:
            list_similars = list(set(list_similars))                    # remove redundancy (duplicates)
            list_not_out_edged = set(list_not_out_edged)                # casting ## should'nt this be remove redundancy instead of casting?

            list_not_in_edged = set(list_asin) - set(list_similars)     # find products with asin but not appearing as similars of others
            list_extern = set(list_similars) - set(list_asin)           # find products appearing as similars but not defined in this dataset file

            total_isolated = list_not_in_edged & list_not_out_edged     # find disconnected nodes

            print("\t\t\t\tASIN : \t\t\t\t\t\t\t" + str(len(list_asin)))
            print("\t\t\t\tSIMILARS (UNIQUES) \t\t\t\t" + str(len(list_similars)))
            print("\t\t\t\tNOT IN-EDGED NODES: \t\t\t" + str(len(list_not_in_edged)))
            print("\t\t\t\tNODES CREATED OUTSIDE (FILE) : \t" + str(len(list_extern)))
            print("\t\t\t\tNOT OUT-EDGED NODES: \t\t\t" + str(int(notOutEdged)))
            print("\t\t\t\tISOLATED NODES: \t\t\t\t" + str(len(total_isolated)), "\n")

        return graph