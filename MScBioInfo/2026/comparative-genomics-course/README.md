# Molecular Evolution - Comparative Genomics

## Contact

Alexandros Pittis ([CGLab](https://cgenomicslab.org/#contact))

## Course structure

### Day 1 — Phylogenetics & the SLC26 family

| Notebook | Topic | Link |
|:---|:---|:---|
| **01** | Phylogenetics basics: orthology/paralogy, ETE3, NCBI taxonomy, MAFFT alignment, trimming | [notebook 1](https://github.com/cgenomicslab/Courses/blob/main/MScBioInfo/2026/comparative-genomics-course/notebooks/01_phylogenetics_basics.ipynb) |
| **02** | SLC26 tree, ETE4 smartview, subfamily identification, prestin extraction, method comparison | [notebook 2](https://github.com/cgenomicslab/Courses/blob/main/MScBioInfo/2026/comparative-genomics-course/notebooks/02_slc26_prestin.ipynb) |

### Day 2 — Convergent evolution

| Notebook | Topic | Link |
|:---|:---|:---|
| **03** | Convergent residue detection, permutation tests, cross-subfamily comparison | will be updated |
| **04** | Domain mapping, structure visualization, functional interpretation | will be updated |

## Data

- `data/cox1.nw` — 3 canonical cox1 sequences from 3 species (headers: `>taxid.accession`), curated from UniProt reference proteomes.
- `data/selection2_clustalo.fa` — 8 canonical SLC23 sequences from 3 species (headers: `>taxid.accession`), curated from UniProt reference proteomes.
- `data/selection2_clustalo.fa` — 297 canonical SLC26 sequences from 30 mammalian species (headers: `>taxid.accession`), curated from UniProt reference proteomes.

## Setup

```bash
conda env create -f environment.yml
conda activate convergent-evo
cd notebooks && jupyter notebook
```

Start with `01_phylogenetics_basics.ipynb`.

## Tools

MAFFT, trimAl, FastTree, IQ-TREE — phylogenetic pipeline
ETE3 (inline rendering) + ETE4 v4.4+ (interactive smartview) — tree visualization
Biopython, pandas, matplotlib, seaborn — sequence & data analysis

## References

- Parker et al. (2013) Nature 502, 228–231
- Bavi et al. (2021) Nature 600, 553–558 (prestin cryo-EM, PDB 7S8X)
- Li et al. (2008) PNAS 105, 13959–13964
- Alper & Sharma (2013) Mol. Aspects Med. 34, 494–515

## Feedback

This is a new course that will improve with your input. After class, we **welcome feedback on pace, clarity, and content**.

