import json
import networkx as nx

class EnrichmentGraph:

    def compute_enrichment(self, file="meta_Books", amazon_meta="amazon-meta", new_amazon_meta="formatted_amazon-meta"):
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
                    print(f'Found ASIN {asin} in amazon-meta.txt file.')
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

        print('Finished writing formatted data to the new file.')

