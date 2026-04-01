# Prestin convergent residues — PyMOL visualization
# Run: pymol prestin_convergent.pml
#
# Replace RESIDUE_LIST with actual convergent site positions
# (mapped to human prestin sequence numbering)

fetch 7S8X, prestin
remove solvent
remove chain B

hide everything
show cartoon, prestin
set cartoon_transparency, 0.3

# Color by domain (approximate boundaries)
color gray80, prestin
color tv_red, prestin and resi 81-505     # TMD
color tv_orange, prestin and resi 506-530  # Linker
color tv_blue, prestin and resi 531-744    # STAS

# Convergent residues (fill in from NB03 results)
# select convergent, prestin and resi RESIDUE_LIST
# show spheres, convergent and name CA
# color yellow, convergent and name CA

bg_color white
orient prestin
