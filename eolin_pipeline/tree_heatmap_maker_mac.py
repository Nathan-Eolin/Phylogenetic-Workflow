#This script is for creating heatmaps and bar graphs for neural subtype expression
import os
import glob
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
import pandas as pd
from io import StringIO
from Bio import Phylo

# Directory containing Newick files
newick_directory = '/Users/Nate/Desktop/newick_trees/'

# Directory to save heatmap and bar graph PNG files
output_directory = '/Users/Nate/Desktop/plots/'

# Load gene expression data from CSV
expression_data_file = '/Users/Nate/Desktop/neuralsub_average_df.csv'
all_expression_data = pd.read_csv(expression_data_file, index_col=0)

# Iterate over files in the directory
for newick_file in glob.glob(os.path.join(newick_directory, '*.newick')):
    # Parse the Newick file to get the selected gene codes
    with open(newick_file, 'r') as f:
        newick_tree = f.read()

    tree = Phylo.read(StringIO(newick_tree), 'newick')
    selected_gene_codes = []
    for clade in tree.get_terminals():
        gene_info = clade.name.split('|')
        species_name, gene_code = gene_info[0].strip(), gene_info[1].strip()
        if species_name == "Clytia_Hemisphaerica_Cnidarian":
            selected_gene_codes.append(gene_code)

    # Filter the selected gene codes based on their presence in both the Newick tree and the loaded expression data
    filtered_gene_codes = [gene_code for gene_code in selected_gene_codes if gene_code in all_expression_data.index]

    # Filter expression data for genes present in both the Newick tree and the loaded CSV file
    selected_expression_data = all_expression_data.loc[filtered_gene_codes]

    # Check if the expression data is empty
    if selected_expression_data.empty:
        print(f"No gene expression data available for {newick_file}. Skipping.")
        continue

    # Get gene names and expression values for selected genes
    gene_names = selected_expression_data.index.tolist()
    expression_values = selected_expression_data.values.tolist()
    cell_type = ["Early Stages", "Cells-A (incl. GLWa, MIH)", "Cells-B (incl. RFamide)", "Cells-C (incl. YFamide)"]

    # Check the number of genes
    num_genes = len(expression_values)
    if num_genes == 1:
        # Create a bar graph instead of a heatmap
        plt.figure(figsize=(12, 8))
        plt.bar(cell_type, expression_values[0], color='blue')
        plt.xlabel('Cell Type')
        plt.ylabel('Gene Expression')
        plt.title('Gene Expression Bar Graph')
        plt.rcParams['font.size'] = 8
    elif num_genes >= 2:
        # Perform hierarchical clustering
        Z = linkage(expression_values, method='average')

        # Create a dendrogram
        dendro = dendrogram(Z, labels=gene_names, no_plot=True)

        # Reorder expression values based on the dendrogram leaves order
        ordered_expression_values = [expression_values[i] for i in dendro['leaves']]

        # Create a heatmap of gene expression
        plt.figure(figsize=(10, 8))
        sns.heatmap(ordered_expression_values, cmap="viridis", xticklabels=cell_type, yticklabels=gene_names, cbar=True, square=True)
        plt.rcParams['font.size'] = 8
        plt.xlabel('Cell Sub-Type')
        plt.title('Gene Expression Heatmap')

    # Save the plot as a PNG file
    filename = os.path.splitext(os.path.basename(newick_file))[0] + '_subtype.png'
    output_path = os.path.join(output_directory, filename)
    plt.savefig(output_path)

    # Close the plot to free up memory
    plt.close()