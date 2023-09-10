from Bio import SeqIO
import os
import glob
from collections import defaultdict

# Input fasta file name
input_file = "/home/eolin117/noma2.fa"

# Output directory for protein sequences
output_dir = "/home/eolin117/hits"

# Maximum number of hits to consider for each species
max_hits_per_species = 15

# Iterate over all hmmscan result files in the output directory
for result_file in glob.glob("/home/eolin117/output/*.txt"):
    try:
        # Determine the name of the gene family from the filename
        gene_family = os.path.splitext(os.path.basename(result_file))[0]

        # Parse hmmscan output to obtain query names and scores
        query_scores = defaultdict(list)
        with open(result_file, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                fields = line.strip().split()
                query_name = fields[2]
                species_name = query_name.split("|")[0]  # extract the species name before the first |
                query_score = float(fields[8])  # Extract the score column value
                query_scores[(species_name, query_name)].append(query_score)

        # Select top hits for each species
        selected_queries = set()
        selected_hits_per_species = defaultdict(list)
        for (species_name, query_name), scores in query_scores.items():
            hits = [(query_name, score) for score in scores]  # Associate each hit with its score
            selected_hits_per_species[species_name].extend(hits)

        for species_name, hits in selected_hits_per_species.items():
            hits.sort(key=lambda x: x[1], reverse=True)  # Sort hits by the score in descending order
            top_hits = hits[:max_hits_per_species]  # Select top max_hits_per_species hits for each species

            for query_name, score in top_hits:
                selected_queries.add((species_name, query_name))
                print(f"Selected hit: {query_name} (Species: {species_name}), Score: {score}")

        print(f"Selected queries for {gene_family}: {len(selected_queries)}")

        # Extract protein sequences for all selected hits from input fasta file
        sequences = {}
        with open(input_file, "r") as f:
            for record in SeqIO.parse(f, "fasta"):
                header = record.id
                species_name = header.split("|")[0]  # extract the species name before the first |
                if (species_name, header) in selected_queries:
                    score = max(query_scores[(species_name, header)])  # Get the maximum score for the hit
                    sequences[header] = (str(record.seq), score)  # Include the score in the sequences dictionary
                    print(f"Extracting protein sequence for {species_name}: {header}")

        # Write protein sequences to output fasta file with scores in the headers
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f"{gene_family}.fasta")

        # Check if the output file already exists
        if os.path.exists(output_file):
            print(f"Output file {output_file} already exists. Skipping writing the fasta file.")
            continue

        with open(output_file, "w") as f:
            for header, (sequence, score) in sequences.items():
                f.write(f">{header}|Score_{score}\n{sequence}\n")  # Add the score after the header using "|" delimiter

        print(f"Wrote {len(sequences)} protein sequences for {gene_family} to {output_file}")

    except IndexError:
        print(f"An IndexError occurred while processing file: {result_file}. Skipping this file.")
        continue
