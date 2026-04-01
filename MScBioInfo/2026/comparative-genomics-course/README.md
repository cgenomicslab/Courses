# Convergent Molecular Evolution in Echolocating Mammals

MSc Bioinformatics — OMICS, University of Crete, 2026

Comparative Genomics Lab (CGLab), IMBB-FORTH

## Setup

```bash
conda env create -f environment.yml
conda activate convergent-evo
```

To update after changes:

```bash
conda env update -f environment.yml --prune
```

## Notebooks

| Notebook | Topic |
|:---|:---|
| **01** | Phylogenetics basics |
| **02** | Comparative genomics |
| **03** | Hypothesis testing — permutation tests |
| **Assignment** | Do convergent sites cluster in protein domains? |

## Resources

### Tutorials
- [Pandas — 10 minutes](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Python Graph Gallery](https://python-graph-gallery.com/)

### Tools
- [ETE4](https://etetoolkit.github.io/ete/)
- [MAFFT](https://mafft.cbrc.jp/alignment/software/)
- [trimAl](http://trimal.cgenomics.org/)
- [FastTree](http://www.microbesonline.org/fasttree/)
- [IQ-TREE](http://www.iqtree.org/)
- [pyMSAviz](https://github.com/moshi4/pyMSAviz)

### Key references
- Parker et al. (2013) Genome-wide signatures of convergent evolution in echolocating mammals. *Nature* 502:228–231
- Zou & Zhang (2015) Are convergent and parallel amino acid substitutions in protein evolution more prevalent than neutral expectations? *Mol Biol Evol* 32:2085–2096
- Thomas & Hahn (2015) Determining the null model for detecting adaptive convergence from genomic data. *Mol Biol Evol* 32:1232–1241
- Rey et al. (2019) Detecting convergent amino acid evolution. *Phil Trans R Soc B* 374:20180234
