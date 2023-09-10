Hello Weissbourd Lab and others

To be able to use this pipeline, you first need an hmm-profile (or multiple) in the hmm_profiles directory. 
	I get my hmm-profiles from the PANTHER database, but you can get yours from wherever you wish as long as the hmm-profiles are built from a good number of species(i.e. not just from vertebrates, get some diversity in there)

You also need to set this up within a conda environment to download all of the required packages necessary for the pipeline.

You can go into the code and edit the paths to fit your directory for where you are running the code on your machine or on an HPC.

By default, MUSCLE is running the super5 algorithm built for a large number of sequences. You can change this if your alignment is not a large number of sequences for optimization 

If you need to run trees faster, look for the fast tree output after the alignment is created.

The code is currently designed to work on the slurm job scheduler in the Engaging HPC at MIT, so if you're running it locally you just need to get rid of all of the slurm options in the new_job_script.sh file.

Happy homology hunting!

To be able to get expression data, you first need to take the average of each gene's expression per cell type as provided with the UCSC Cell Browser