# Assignment — Do convergent sites cluster in any protein domain?

## Background

We identified alignment positions where echolocating
mammals show significantly higher amino acid agreement than expected
by chance — these are **convergent sites**:.

Human prestin (SLC26A5) has the following approximate domain structure:

| Domain | Alignment positions | Function |
|:---|:---|:---|
| N-terminal | 0 – 79 | Cytoplasmic, regulatory |
| TMD (transmembrane) | 80 – 504 | Motor domain, 14 TM helices |
| Linker | 505 – 529 | Connects TMD to STAS |
| STAS domain | 530 – end | C-terminal regulatory |

*Approximate boundaries in the alignment coordinate system.*

## ToDo

Make a **Jupyter notebook** that answers:

> **Are convergent sites enriched in any specific protein domain?**

First, test whether the **TMD** contains more
convergent sites than expected by chance. Consider checking also the other domains

Create a Jupyter notebook that answers this question using a
**permutation test**. Your notebook should:

1. **Load the convergence results** (`https://raw.githubusercontent.com/cgenomicslab/Courses/refs/heads/main/MScBioInfo/2026/comparative-genomics-course/data/prestin_convergence_results.csv`)
2. **Define protein domains** (TMD: ~81–505, STAS: ~531–744, other)
3. **Count** how many convergent sites (p < 0.05) fall in the TMD
4. **Build a null distribution**: if the same number of sites were
   randomly placed across the protein, how many would fall in the TMD
   by chance? Repeat 10,000 times.
5. **Compute a p-value** and make a plot showing the null distribution
   with the observed count marked
6. **Interpret** briefly

## Deliverables

- A Jupyter notebook (`.ipynb`) with all code, plots, and interpretation
- Save it after "running all"
