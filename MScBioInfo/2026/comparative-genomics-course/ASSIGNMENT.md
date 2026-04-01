# Assignment — Do Convergent Sites Cluster in the Transmembrane Domain?

## Background

In Notebook 3 we identified alignment positions where echolocating
species show convergent amino acid usage in prestin (SLC26A5).

Biological question: **are these convergent sites randomly
scattered across the protein, or do they cluster in the transmembrane
motor domain (TMD)?**

Prestin's motor function lies in the TMD (approximately residues
81–505 in human prestin). If there is selection for improved echolocation, 
we'd expect convergent sites to be **enriched** in the TMD.

## ToDo

Create a Jupyter notebook that answers this question using a
**permutation test**. Your notebook should:

1. **Load the convergence results** from Notebook 3
   (`data/prestin_convergence_results.csv`)
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
- Make the notebook run from start to finish without errors
- Save it after "running all"
