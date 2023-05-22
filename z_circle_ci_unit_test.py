import os
import matplotlib as mpl
from enrichment.enrichment_graph import EnrichmentGraph
from explore.exploration_graph import ExploreGraph
from persistence.persistence_graph import PersistenceGraph
from visualization.visualization_graph import VisualizationGraph
from analytics.analytics_graph import AnalyticsGraph
from preprocessing.pre_processing_graph import PreProcessGraph

if __name__ == '__main__':
    print("\n=========================================================================================")
    print("========================INFLUENCE=OF=POPULARITY=ON=SALES===UNI-FR========================")
    print("==================================UNIT=TEST=CIRCLE_CI====================================\n")

    if os.name == "nt":
        mpl.use('TkAgg')
        print("Windows profile has been loaded.")
    elif os.name == "posix":
        print("Mac profile has been loaded.")
    else:
        print("Unknown operating system.")

    eg, pg, ag, vg, er, db = ExploreGraph(), PreProcessGraph(), AnalyticsGraph(), VisualizationGraph(), EnrichmentGraph(), PersistenceGraph()


    print(">>Display all information and steps of all our project ********************************************\n\n")

    # CONSTRUCTION OF THE GRAPH ====================================================================================
    graph_sampled_small = eg.construct_graph_by_file(file_name="./dataset/dataset_off_amazon_test.txt")

    # QUALITY OF THE GRAPH =========================================================================================
    pg.display_efficiency_of_graph(graph=graph_sampled_small)

    print(">>Display all information and steps of the community detection ************************************\n\n")

    # COMMUNITY DETECTION===========================================================================================
    communities = ag.amazon_community_detection(graph=graph_sampled_small, tag="overall_scenario", run_silhouette=False, display=False, sub_function=False)
    communities_library = ag.community_library_detection(graph=graph_sampled_small, library="louvain", display=False)

    # POPULAR ======================================================================================================
    popular_nodes = ag.highest_betweenness_centralities(graph=graph_sampled_small, communities=communities, display=False)

    # QUALITY=====ACCURACY=PRECISION=RECALL=JACCARD=================================================================
    acc, pre, rec, jac = ag.accuracy_precision_recall_jaccard(communities_library=communities_library, community_homemade=communities, display=False)

    # QUALITY=====SILHOUETTE========================================================================================
    silhouette_homemade = ag.silhouette_score(graph=graph_sampled_small, communities=communities, metric="euclidean", sample_size=100, sub_function=False)

    # EXPLORATION OF THE GRAPH =====================================================================================
    eg.analytics_exploration(graph=graph_sampled_small, display=False)

    # SIMULATE ENRICHMENT===========================================================================================
    er.compute_enrichment(file="meta_Books", amazon_meta="test", new_amazon_meta="test")
    merged = er.merge_for_enrichment(original_graph=graph_sampled_small, enrichment_file="formatted_amazon_meta.txt")

    # CHECK DB======================================================================================================
    db.display_community(community_id=1, communities=communities)

    # DISPLAY ALL COMMUNITY IN DIFFERENT COLOR WITH POPULAR NODE (CENTROID) IN GOLD COLOR ==========================
    vg.display_communities_graph(graph=graph_sampled_small, communities=communities, populars=popular_nodes, display=False, tag="overall_scenario_plot")

    # DISPLAY THE DEGREE DISTRIBUTION OF THE EDGES IN THE GRAPH ====================================================
    vg.degree_distribution(graph=graph_sampled_small, display=False, tag="overall_scenario_distribution")

    # DISPLAY EACH COMMUNITY (FOR SAKE OF TIME ONLY 3) ============================================================
    limit, number_to_display = 0, 3
    for community in communities:
        if limit >= number_to_display:
            break
        eg.explore_community(graph=graph_sampled_small, community=community, display=False)
        limit += 1
