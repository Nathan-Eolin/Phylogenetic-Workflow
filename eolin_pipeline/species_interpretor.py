import os
import re

# Define a dictionary that maps species codes to species names
code_to_name = {
    "c_hem": "Clytia_Hemisphaerica_Cnidarian",
	"Hs": "Homo_Sapiens_Chordate",
	"Ta": "Trichoplax_adhaerens_Placozoa",
	"s_ros": "Salpingoeca_rosetta_Choanoflagellate",
	"Sp": "Strongylocentrotus_purpuratus_Echinoderm",
	"s_cer": "Saccharomyces_cerevisiae_Fungus",
	"Pd": "Pocillopora_damicornis_Cnidarian",
	"Of": "Orbicella_faveolata_Cnidarian",
	"m_bre": "Monosiga_brevicollis_Choanoflagellate",
	"La": "Lingula_anatina_Brachiopod",
	"Hv": "Hydra_vulgaris_Cnidarian",
	"Dm": "Drosophila_melanogaster_Insect",
	"Ct": "Capitella_teleta_Annelid",
	"Ci": "Ciona_intestinalis_Chordate",
	"Cg": "Crassostrea_gigas_Mollusk",
	"Aq": "Amphimedon_queenslandica_Poriferan",
	"Ad": "Acropora_digitifera_Cnidarian",
	"Ac": "Aplysia_californica_Mollusk",
	"a_aur": "Aurelia_aurita_Cnidarian",
	"Bf": "Branchiostoma_floridae_Chordate",
	"Ce": "Caenorhabditis_elegans_Nematode",
	"c_owc": "Capsaspora_owczarzaki_Filasterea",
	"Sk": "Saccoglossus_kowalevskii_Hemichordate",
	"Nv": "Nematostella_vectensis_Cnidarian",
	"Ep": "Exaiptasia_pallida_Cnidarian",
	"m_lei": "Mnemiopsis_leidyi_Ctenophore"
	"d_gig": "Dendronephthya_gigante_Cnidarian"
	"p_nak": "Praesagittifera_naikaiensis_Xencoel",
	"ast": "Astroides_calycularis_Cnidarian"#** bit sensitive publication wise
	"m_vir": "Morbakka_virulenta_Cnidarian"
	"Pa": "Phoronis_australensis_Phoronida"
	"Pc": "Priapulus_caudatus",
	"Xb": "Xenoturbella_bocki_Xencoel",#** bit sensitive publication wise
	"sb": "Pleurobrachia_bachei_Ctenophore",


}

#regular expression pattern to match species codes in the newick tree
code_pattern = re.compile(r"([A-Za-z_]+)\|")

folder_path = "trees"

for filename in os.listdir(folder_path):
    if filename.endswith(".newick.treefile"):
        # Construct the paths to the input and output files
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(folder_path, filename.replace(".newick.treefile", ".newick"))
        
        # Open the input and output files
        with open(input_path, "r") as input_file, open(output_path, "w") as output_file:
            # Read in the input tree
            input_tree = input_file.read()
            
            # Replace the species codes with their corresponding names using the code-to-name mapping
            output_tree = code_pattern.sub(lambda match: code_to_name.get(match.group(1), match.group(1)) + "|", input_tree)
            
            # Write the updated tree to the output file
            output_file.write(output_tree)