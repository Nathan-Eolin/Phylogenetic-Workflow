#!/bin/bash

alignment_dir="alignments"
output_dir="Fasttree"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate through each alignment file in the directory
for alignment_file in "$alignment_dir"/*.afa; do
    # Get the base filename without the extension
    filename=$(basename "$alignment_file")
    filename="${filename%.*}"

    # Define the output filename
    output_file="$output_dir/${filename}_aln_fasttree.newick"

    # Apply the command to the alignment file
    Fasttree "$alignment_file" > "$output_file"

    # Print a message indicating the completion of the command
    echo "Command applied to $alignment_file. Output saved to $output_file"
done
