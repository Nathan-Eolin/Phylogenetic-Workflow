#!/bin/bash

#SBATCH --job-name=eolinjob
#SBATCH -N 16
#SBATCH -n 128
#SBATCH --mem=25GB
#SBATCH --ntasks-per-node=8
#SBATCH --time=12:00:00
#SBATCH --partition=sched_mit_hill
#SBATCH --constraint=centos7
#SBATCH --error=error.txt

# Error file
error_file="error.txt"

# Activate conda environment
source /home/eolin117/miniconda3/etc/profile.d/conda.sh
conda activate base

# Input files
fasta_file="/home/eolin117/noma2.fa"
hmm_dir="/home/eolin117/hmm_profiles"

# Output directory
out_dir="/home/eolin117/output"
algn_dir="/home/eolin117/alignments"
trimmed_dir="/home/eolin117/trimmed_algn"
hits_dir="/home/eolin117/hits"
tree_dir="/home/eolin117/trees"

# Create the directories if they don't exist
mkdir -p /home/eolin117/output
mkdir -p /home/eolin117/alignments
mkdir -p /home/eolin117/trimmed_algn
mkdir -p /home/eolin117/hits
mkdir -p /home/eolin117/trees

# Iterate over all HMM profiles in directory
for file in $hmm_dir/*.hmm
do
    # Create binary HMM file
    hmmpress $file

    # Run hmmscan to search for hits
    base=$(basename $file .hmm)
    out_file="$out_dir/${base}_hits.txt"
    # Check if output file exists
    if [ -f "$out_file" ]; then
      echo "Skipping $file: Output file already exists"
    else
      hmmscan -E 1e-10 --tblout $out_file $file $fasta_file
    fi
done

# Extract the protein sequences to match with the hmmscan hits
python /home/eolin117/hmm_parser.py

# Set the parameters for the sbatch job
job_name="eolinjob"
nodes=16
tasks_per_node=8
total_tasks=$((nodes*tasks_per_node))
mem="25GB"
time="12:00:00"
partition="sched_mit_hill"
constraint="centos7"

# Set the IQtree parameters
model="MFP+MERGE"
bootstrap=1000
alrt=1000
nt="AUTO"

# Iterate over all fasta files in the hits directory
for file in $hits_dir/*.fasta
do
    alignment_file="$algn_dir/$(basename $file .fasta)_aln.afa"
    tree_file="$tree_dir/$(basename $file .fasta)_tree.newick"
    tree_file_output="$tree_dir/$(basename $file .fasta)_tree.newick.treefile"
    trimmed_file="$trimmed_dir/$(basename $file .fasta)_aln.clipkit"

    # Check if both alignment and tree files exist
    if [ -f "$alignment_file" ] && [ -f "$tree_file_output" ]; then
      echo "Skipping $file: Output files already exist"
    else
      # Create the job script file
      sbatch_file="/home/eolin117/tree_scripts/$(basename "${file}" .fasta).sh"
      echo "#!/bin/bash" > $sbatch_file
      echo "#SBATCH --job-name=$job_name" >> $sbatch_file
      echo "#SBATCH -N $nodes" >> $sbatch_file
      echo "#SBATCH -n $total_tasks" >> $sbatch_file
      echo "#SBATCH --ntasks-per-node=$tasks_per_node" >> $sbatch_file
      echo "#SBATCH --mem=$mem" >> $sbatch_file
      echo "#SBATCH --time=$time" >> $sbatch_file
      echo "#SBATCH --partition=$partition" >> $sbatch_file
      echo "#SBATCH --constraint=$constraint" >> $sbatch_file
      echo "#SBATCH --error=$error_file" >> $sbatch_file
      echo "" >> $sbatch_file
      echo "source /home/eolin117/miniconda3/etc/profile.d/conda.sh" >> $sbatch_file
      echo "conda activate base" >> $sbatch_file
      echo "" >> $sbatch_file
      echo "if [ ! -f \"$alignment_file\" ]; then" >> $sbatch_file
      echo "  muscle -super5 $file -output $alignment_file" >> $sbatch_file
      echo "  clipkit $alignment_file -o $trimmed_file" >> $sbatch_file
      echo "fi" >> $sbatch_file
      echo "" >> $sbatch_file
      echo "if [ ! -f \"$tree_file\" ]; then" >> $sbatch_file
      echo "  iqtree -s $trimmed_file -m $model -fast -nt $nt -pre $tree_file" >> $sbatch_file
      echo "fi" >> $sbatch_file

      # Submit the sbatch job
      sbatch $sbatch_file
    fi
done

