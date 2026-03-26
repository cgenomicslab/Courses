# Convergent Molecular Evolution in Echolocating Mammals

A 2-day computational biology module for MSc Bioinformatics (2026), using the SLC26 anion transporter family to detect convergent evolution in echolocating bats and dolphins.

Based on [Parker et al. (2013)](https://www.nature.com/articles/nature12511) — *Genome-wide signatures of convergent evolution in echolocating mammals*, Nature 502, 228–231.

## Why SLC26?

The SLC26 family has 11 members sharing the same domain architecture (Sulphate_transp + STAS). Only **SLC26A5 (prestin)** is a cochlear motor protein essential for echolocation — every other subfamily is a built-in negative control.

## Course structure

### Day 1 — Phylogenetics & the SLC26 family

| Notebook | Topic |
|:---|:---|
| **01** | Phylogenetics basics: orthology/paralogy, ETE3, NCBI taxonomy, MAFFT alignment, trimming |
| **02** | SLC26 tree, ETE4 smartview, subfamily identification, prestin extraction, method comparison |

### Day 2 — Convergent evolution

| Notebook | Topic |
|:---|:---|
| **03** | Convergent residue detection, permutation tests, cross-subfamily comparison |
| **04** | Domain mapping, structure visualization, functional interpretation |

## Data

`data/selection2_clustalo.fa` — 297 canonical SLC26 sequences from 30 mammalian species (headers: `>taxid.accession`), curated from UniProt reference proteomes using `scripts/uniprot_phylo.py`.

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
Biopython, pandas, matplotlib — sequence & data analysis

## References

- Parker et al. (2013) Nature 502, 228–231
- Bavi et al. (2021) Nature 600, 553–558 (prestin cryo-EM, PDB 7S8X)
- Li et al. (2008) PNAS 105, 13959–13964
- Alper & Sharma (2013) Mol. Aspects Med. 34, 494–515
