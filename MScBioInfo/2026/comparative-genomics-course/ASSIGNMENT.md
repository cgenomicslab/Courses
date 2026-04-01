# Assignment — Do Convergent Sites Cluster in the Transmembrane Domain?

## Background

In Notebook 3 you identified alignment positions where echolocating
species show convergent amino acid usage in prestin (SLC26A5).

Now the biological question: **are these convergent sites randomly
scattered across the protein, or do they cluster in the transmembrane
motor domain (TMD)?**

Prestin's motor function resides in the TMD (approximately residues
81–505 in human prestin). If convergent evolution is driven by
selection for improved echolocation, we'd expect convergent sites
to be **enriched** in the TMD.

## Your task

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
6. **Interpret** your result in 2–3 sentences

## Deliverables

- A Jupyter notebook (`.ipynb`) with all code, plots, and interpretation
- The notebook should run from start to finish without errors

## Hints

- You already know how to do permutation tests from Notebook 3
- Think about what you're shuffling: the *positions* of convergent
  sites, not the amino acids themselves

## Evaluation

- Correctness of the statistical test
- Quality of the visualization
- Clarity of the interpretation
