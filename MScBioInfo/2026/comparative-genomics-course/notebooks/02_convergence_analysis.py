# %% [markdown]
# # Lesson 2: From Sequence Alignments to Hypothesis Testing
#
# In Lesson 1 we built a multiple sequence alignment of the **SLC26 anion
# transporter family** — ~297 protein sequences across 30 mammalian species.
# Today we'll turn that alignment into *data* we can analyze statistically.
#
# **Our biological question:** Bats and dolphins evolved echolocation
# independently. Did their **prestin** proteins — the cochlear motor protein
# responsible for sound amplification — converge to similar amino acid
# sequences? And can we test this statistically?
#
# **What you'll learn today:**
# 1. How to work with alignment data using **pandas**
# 2. **Shannon entropy** — measuring conservation across alignment positions
# 3. How **permutation tests** work (and what p-values really mean)
# 4. Testing for **convergent evolution** at specific alignment positions

# %% [markdown]
# ---
# ## 1. Setup

# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import math

sns.set_theme()

DATA = os.path.join('..', 'data')

# %% [markdown]
# We'll reuse the simple FASTA reader from Lesson 1:

# %%
def read_fasta(path):
    """Read a FASTA file → dict of {header: sequence}."""
    seqs = {}
    header = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                header = line[1:].split()[0]
                seqs[header] = ''
            elif header:
                seqs[header] += line
    return seqs

# %% [markdown]
# ---
# ## 2. The SLC26 family: context
#
# The SLC26 family has ~10 subfamilies (A1 through A11). Each has a
# different physiological role — sulfate transport, chloride/bicarbonate
# exchange, and so on. The one we care about is **SLC26A5 (prestin)**,
# which is unique: it's a motor protein in the cochlea that amplifies
# sound vibrations.
#
# In Lesson 1 we built a tree of the entire family. I extracted the
# **prestin clade** from that tree and re-aligned those sequences
# with MAFFT, then trimmed the alignment. That's what we'll work with.

# %%
# Quick look at the family tree (instructor demo)
# If this doesn't work on your machine, don't worry — just follow along.
try:
    from ete4 import PhyloTree

    FAMILY_TREE = os.path.join(DATA, 'selection2.clustalo.gt01.fasttree.nwk')
    if os.path.exists(FAMILY_TREE):
        t = PhyloTree(open(FAMILY_TREE).read())
        t.set_outgroup(t.get_midpoint_outgroup())
        print(f"Family tree: {len(list(t.leaves()))} sequences")
        print("Launching interactive viewer...")
        t.explore(name="SLC26 family", keep_server=False)
    else:
        print(f"Tree file not found at {FAMILY_TREE}")
        print("(This is fine — we'll work with the prestin alignment directly.)")
except ImportError:
    print("ETE4 not installed — skipping tree visualization.")

# %% [markdown]
# The key thing to notice in the tree: each subfamily forms a distinct
# clade. The **prestin (A5) clade** has one sequence per species — about
# 30 sequences total. That's the dataset for today.

# %% [markdown]
# ---
# ## 3. Loading the prestin alignment

# %%
PRESTIN_ALN = os.path.join(DATA, 'subfamilies', 'SLC26A5.trim.fasta')
prestin = read_fasta(PRESTIN_ALN)

print(f"Sequences:        {len(prestin)}")
print(f"Alignment length: {len(list(prestin.values())[0])} positions")
print()

# Show the first few
for header, seq in list(prestin.items())[:5]:
    print(f"  {header:<25s}  {seq[:50]}...")

# %% [markdown]
# Each header is formatted as `taxid.accession`. The **taxid** (NCBI
# taxonomy ID) tells us which species this sequence belongs to.

# %% [markdown]
# ---
# ## 4. Working with data in pandas
#
# **pandas** is the standard Python library for working with tabular data.
# We'll convert our alignment into a pandas **DataFrame** — a table where
# each row is a species and each column is an alignment position.
#
# This is the bridge from "bioinformatics" to "data analysis."

# %% [markdown]
# ### 4.1 Creating a DataFrame

# %%
headers = list(prestin.keys())
sequences = list(prestin.values())

# Convert each sequence string into a list of characters
matrix = [list(seq) for seq in sequences]

# Create the DataFrame
aln = pd.DataFrame(matrix, index=headers)
aln.columns.name = 'position'

print(f"Shape: {aln.shape}")
print(f"  → {aln.shape[0]} rows (sequences)")
print(f"  → {aln.shape[1]} columns (alignment positions)")

# %%
# .head() shows the first few rows
aln.head(3)

# %% [markdown]
# Each cell contains a single amino acid (or a gap `-`).

# %% [markdown]
# ### 4.2 Selecting data
#
# pandas lets you select rows, columns, or both.

# %%
# Select a single column → one alignment position
# This returns a Series (like a labeled list)
aln[100]

# %%
# Count how many times each amino acid appears at position 100
aln[100].value_counts()

# %%
# Select several columns → a region of the alignment
aln[[50, 51, 52, 53, 54]]

# %%
# Select a single row → one species' sequence
# Use .iloc[row_number] to select by position (0-based)
aln.iloc[0]

# %% [markdown]
# ### 4.3 Species information
#
# Let's connect each sequence to its species and echolocation status.

# %%
# Load species classification (pre-filled)
species_df = pd.read_csv(
    os.path.join(DATA, 'species_classification.tsv'),
    sep='\t', comment='#',
    names=['taxid', 'species', 'group', 'echolocates', 'notes']
)
species_df['taxid'] = species_df['taxid'].astype(str)

# Quick look
species_df.head()

# %%
# Build lookup dictionaries
echo_lookup = dict(zip(species_df['taxid'], species_df['echolocates']))
name_lookup = dict(zip(species_df['taxid'], species_df['species']))

# What species are in our prestin alignment?
print(f"{'Header':<25s}  {'Species':<35s}  Echo?")
print('-' * 70)
for h in aln.index:
    taxid = h.split('.')[0]
    species = name_lookup.get(taxid, '?')
    echo = echo_lookup.get(taxid, '?')
    marker = ' 🔊' if echo == 'yes' else ''
    print(f"  {h:<25s}  {species:<35s}  {echo}{marker}")

# %% [markdown]
# ### 4.4 Boolean indexing
#
# One of the most powerful features in pandas: selecting rows based on
# a **condition**.

# %%
# Create a True/False series: is this species an echolocator?
taxids = [h.split('.')[0] for h in aln.index]
is_echo = pd.Series(
    [echo_lookup.get(t) == 'yes' for t in taxids],
    index=aln.index
)

# How many?
print(f"Echolocating species:     {is_echo.sum()}")
print(f"Non-echolocating species: {(~is_echo).sum()}")

# %%
# Boolean indexing: select ONLY echolocator rows
echo_aln = aln[is_echo]
echo_aln.head()

# %%
# The tilde ~ means "NOT" — select non-echolocators
other_aln = aln[~is_echo]
other_aln.head()

# %% [markdown]
# ### ✏️ Exercise 1
#
# Pick an alignment position of your choice (try a few). For that position:
#
# 1. What amino acids do the **echolocators** have? Use `echo_aln[pos].value_counts()`.
# 2. What about the **non-echolocators**? Use `other_aln[pos].value_counts()`.
# 3. Can you find a position where echolocators all (or mostly) share the
#    same amino acid, but non-echolocators are more diverse?
#
# *(Hint: try positions in the range 200–400.)*

# %%
# Your code here
pos = 300  # ← change this and explore!
print("Echolocators:")
print(echo_aln[pos].value_counts())
print()
print("Non-echolocators:")
print(other_aln[pos].value_counts())

# %% [markdown]
# ---
# ## 5. Shannon entropy — measuring conservation
#
# Some alignment positions are highly **conserved** (every species has the
# same amino acid) while others are **variable**. We can quantify this
# with **Shannon entropy**:
#
# $$H = -\sum_{i} p_i \cdot \log_2(p_i)$$
#
# where $p_i$ is the frequency of amino acid $i$ at that position.
#
# - $H = 0$: perfectly conserved (one amino acid, probability = 1)
# - $H \approx 4.3$: maximally variable (all 20 amino acids equally frequent)

# %% [markdown]
# ### 5.1 Computing entropy for one position

# %%
# Let's compute entropy at position 100 step by step
col = list(aln[100])

# Remove gaps
residues = [aa for aa in col if aa != '-']
print(f"Residues (no gaps): {len(residues)}")

# Count each amino acid
counts = Counter(residues)
print(f"Counts: {dict(counts)}")

# Compute frequencies
total = len(residues)
for aa, count in counts.items():
    print(f"  {aa}: {count}/{total} = {count/total:.3f}")

# %%
# Now the entropy formula
entropy = 0.0
for count in counts.values():
    p = count / total
    entropy -= p * math.log2(p)

print(f"Shannon entropy at position 100: {entropy:.3f}")

# %% [markdown]
# ### ✏️ Exercise 2
#
# Compute the entropy by hand for a position where **all species have
# the same amino acid**. What do you get? Why?
#
# Then try a position where amino acids are split roughly 50/50 between
# two residues. What's the entropy?

# %% [markdown]
# ### 5.2 Entropy across the whole alignment

# %%
def shannon_entropy(column):
    """Shannon entropy of a list of amino acids (ignoring gaps)."""
    residues = [aa for aa in column if aa != '-']
    if len(residues) == 0:
        return 0.0
    counts = Counter(residues)
    total = len(residues)
    H = 0.0
    for count in counts.values():
        p = count / total
        H -= p * math.log2(p)
    return H

# %%
# Compute entropy at every position
n_positions = aln.shape[1]
entropies = [shannon_entropy(list(aln[pos])) for pos in range(n_positions)]

print(f"Computed entropy for {n_positions} positions")
print(f"  Min entropy: {min(entropies):.3f}  (most conserved)")
print(f"  Max entropy: {max(entropies):.3f}  (most variable)")
print(f"  Mean entropy: {np.mean(entropies):.3f}")

# %%
# Plot the conservation profile
fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(range(n_positions), entropies, linewidth=0.5, color='steelblue')
ax.set_xlabel('Alignment position')
ax.set_ylabel('Shannon entropy (bits)')
ax.set_title('Prestin (SLC26A5) — conservation profile')
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
plt.tight_layout()
plt.show()

# %% [markdown]
# **Valleys** in this plot = highly conserved regions (low entropy).
# These are likely important for protein function.

# %% [markdown]
# ### ✏️ Exercise 3
#
# 1. How many positions have entropy = 0 (perfectly conserved)?
#    ```python
#    sum(1 for e in entropies if e == 0.0)
#    ```
# 2. What fraction of the alignment is that?
# 3. Find the 10 most conserved positions (lowest non-zero entropy).
#    What amino acids are at those positions?

# %%
# Your code here


# %% [markdown]
# ---
# ## 6. Permutation tests — the concept
#
# We want to ask: *"Do echolocators share the same amino acid at certain
# positions more than you'd expect by chance?"*
#
# To answer this, we need a way to compute **p-values**. Instead of
# relying on mathematical formulas (like the t-test), we'll use a
# **permutation test**: a simple, powerful method that works by
# **shuffling the data**.
#
# Let's build the idea step by step, starting with a toy example.

# %% [markdown]
# ### 6.1 A toy example
#
# Imagine you measured some quantity for 15 animals. Five of them belong
# to a group you care about. You notice that those 5 have a higher
# average than the other 10. But is the difference **real**, or could
# it be just luck?

# %%
# Our 15 measurements
values = np.array([12, 18, 11, 19, 17, 20, 10, 13, 9, 14, 8, 11, 13, 21, 10])

# Indices of the 5 "special" animals
special = [1, 3, 4, 5, 13]

# Observed means
special_vals = values[special]
other_vals = np.delete(values, special)

print(f"Special group mean:  {special_vals.mean():.2f}")
print(f"Other group mean:    {other_vals.mean():.2f}")

obs_diff = special_vals.mean() - other_vals.mean()
print(f"Observed difference: {obs_diff:.2f}")

# %% [markdown]
# The "special" group averages 19.0 vs 11.0 for the rest. That's a big
# difference — **but is it significant?**
#
# The logic of a permutation test:
# 1. **Assume the labels don't matter** (this is the "null hypothesis")
# 2. Randomly shuffle which 5 animals are "special"
# 3. Recompute the mean difference
# 4. Repeat many times → build a **null distribution**
# 5. See how often the shuffled difference is as big as the real one

# %% [markdown]
# ### 6.2 One shuffle

# %%
# Randomly pick 5 indices (out of 15) as "special"
np.random.seed(42)  # for reproducibility

shuffled_idx = np.random.choice(15, size=5, replace=False)
print(f"Shuffled 'special' indices: {shuffled_idx}")

shuffled_special = values[shuffled_idx]
shuffled_other = np.delete(values, shuffled_idx)

shuffled_diff = shuffled_special.mean() - shuffled_other.mean()
print(f"Shuffled difference: {shuffled_diff:.2f}")

# %% [markdown]
# One shuffle gave us a difference of {shuffled_diff:.2f}. Let's do many.

# %% [markdown]
# ### 6.3 Many shuffles → the null distribution

# %%
n_permutations = 10000
null_diffs = np.zeros(n_permutations)

for i in range(n_permutations):
    idx = np.random.choice(15, size=5, replace=False)
    null_diffs[i] = values[idx].mean() - np.delete(values, idx).mean()

print(f"Ran {n_permutations} permutations")
print(f"Null distribution: mean = {null_diffs.mean():.3f}, std = {null_diffs.std():.3f}")

# %% [markdown]
# ### 6.4 Visualize and compute the p-value

# %%
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(null_diffs, bins=50, color='lightblue', edgecolor='white')
ax.axvline(obs_diff, color='red', linewidth=2, label=f'Observed = {obs_diff:.2f}')
ax.set_xlabel('Difference in means')
ax.set_ylabel('Count')
ax.set_title('Null distribution (10,000 permutations)')
ax.legend()
plt.tight_layout()
plt.show()

# %%
# The p-value: how often is the null difference ≥ the observed?
p_value = np.mean(null_diffs >= obs_diff)
print(f"P-value: {p_value:.4f}")

# %% [markdown]
# **Interpretation:** The p-value tells you the probability of seeing a
# difference as large as your observed one **if the labels were meaningless**.
#
# A small p-value (typically < 0.05) means the observed difference is
# unlikely under random labeling — the effect is probably real.

# %% [markdown]
# ### ✏️ Exercise 4
#
# 1. Change the number of permutations from 10,000 to 100, 1,000, and
#    100,000. How does the p-value change? Does it stabilize?
#
# 2. Replace `np.mean` with `np.median` in the test statistic.
#    Does the conclusion change?
#
# 3. What happens if you make the "special" values less extreme?
#    Try replacing `values` with numbers where the groups are more similar.

# %%
# Your code here


# %% [markdown]
# ---
# ## 7. From numbers to amino acids
#
# In the toy example we compared **means** of two groups. But amino acids
# are **categorical** — we can't compute a mean of {A, N, N, S}.
#
# Instead, we ask: **do the echolocators "agree" on the same amino acid
# more than expected by chance?**

# %% [markdown]
# ### 7.1 An "agreement score"
#
# For a group of species, the agreement score at a position is simply:
#
# $$\text{agreement} = \frac{\text{count of the most common amino acid}}{\text{group size}}$$
#
# If all echolocators have Asparagine (N), the score is 1.0.
# If they're split evenly between N, S, and T, the score is ~0.33.

# %%
def agreement_score(amino_acids):
    """Fraction of the group sharing the most common amino acid."""
    # Remove gaps
    residues = [aa for aa in amino_acids if aa != '-']
    if len(residues) == 0:
        return 0.0
    most_common_count = Counter(residues).most_common(1)[0][1]
    return most_common_count / len(residues)

# %%
# Example: echolocator amino acids at position 300
echo_aas = list(echo_aln[300])
other_aas = list(other_aln[300])

echo_score = agreement_score(echo_aas)
other_score = agreement_score(other_aas)

print(f"Position 300:")
print(f"  Echolocators:      {echo_aas}")
print(f"  Agreement score:   {echo_score:.3f}")
print()
print(f"  Non-echolocators:  {other_aas}")
print(f"  Agreement score:   {other_score:.3f}")

# %% [markdown]
# ### 7.2 Permutation test on one position
#
# Same logic as the toy example:
# 1. Compute the **observed** agreement score for echolocators
# 2. Shuffle: randomly label N species as "echolocators"
# 3. Recompute the agreement score
# 4. Repeat → null distribution → p-value

# %%
# Get ALL amino acids at this position (both groups combined)
pos = 300
all_aas = list(aln[pos])

# How many echolocators?
n_echo = int(is_echo.sum())
n_total = len(all_aas)

# Observed score
obs_score = agreement_score([all_aas[i] for i in range(n_total) if is_echo.iloc[i]])
print(f"Observed echolocator agreement at position {pos}: {obs_score:.3f}")

# %%
# Permutation test
n_perm = 10000
null_scores = np.zeros(n_perm)

for i in range(n_perm):
    # Shuffle: randomly pick n_echo species as "echolocators"
    fake_echo_idx = np.random.choice(n_total, size=n_echo, replace=False)
    fake_echo_aas = [all_aas[j] for j in fake_echo_idx]
    null_scores[i] = agreement_score(fake_echo_aas)

p_value = np.mean(null_scores >= obs_score)

print(f"P-value at position {pos}: {p_value:.4f}")

# %%
# Visualize
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(null_scores, bins=30, color='lightblue', edgecolor='white')
ax.axvline(obs_score, color='red', linewidth=2,
           label=f'Observed = {obs_score:.3f}')
ax.set_xlabel('Agreement score')
ax.set_ylabel('Count')
ax.set_title(f'Permutation test at position {pos}')
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ### ✏️ Exercise 5
#
# 1. Try different alignment positions. Can you find one with a very
#    low p-value (p < 0.01)?
# 2. Can you find one where echolocators are clearly NOT converging
#    (high p-value)?
# 3. What happens at positions that are perfectly conserved (entropy = 0)?
#    Is the agreement score high? Is the p-value low? Why or why not?

# %%
# Your code here


# %% [markdown]
# ---
# ## 8. Scanning the whole alignment
#
# Now we're ready for the real analysis: run the permutation test at
# **every position** and see where convergence signals appear.

# %% [markdown]
# ### 8.1 A function that runs the test

# %%
def convergence_pvalue(aln, is_echo, pos, n_perm=1000):
    """
    Permutation test for convergence at one alignment position.

    Returns the agreement score for echolocators and the p-value.
    """
    all_aas = list(aln[pos])
    n_echo = int(is_echo.sum())
    n_total = len(all_aas)

    # Observed score
    echo_aas = [all_aas[i] for i in range(n_total) if is_echo.iloc[i]]
    obs = agreement_score(echo_aas)

    # Null distribution
    count_as_extreme = 0
    for _ in range(n_perm):
        idx = np.random.choice(n_total, size=n_echo, replace=False)
        null_score = agreement_score([all_aas[j] for j in idx])
        if null_score >= obs:
            count_as_extreme += 1

    p = count_as_extreme / n_perm
    return obs, p

# %%
# Test it on a single position
score, pval = convergence_pvalue(aln, is_echo, pos=300, n_perm=5000)
print(f"Position 300: agreement = {score:.3f}, p = {pval:.4f}")

# %% [markdown]
# ### 8.2 Scan all positions
#
# This will take a minute or two — we're running 1,000 permutations at
# each of ~700 positions.

# %%
n_positions = aln.shape[1]
results = []

print(f"Scanning {n_positions} positions (1,000 permutations each)...")
for pos in range(n_positions):
    score, pval = convergence_pvalue(aln, is_echo, pos, n_perm=1000)
    results.append({'position': pos, 'agreement': score, 'pvalue': pval})

    # Progress indicator every 100 positions
    if (pos + 1) % 100 == 0:
        print(f"  ... {pos + 1}/{n_positions}")

results_df = pd.DataFrame(results)
print("Done!")

# %%
# Quick summary
n_sig = (results_df['pvalue'] < 0.05).sum()
print(f"Positions with p < 0.05:  {n_sig} / {n_positions}")
print(f"Positions with p < 0.01:  {(results_df['pvalue'] < 0.01).sum()} / {n_positions}")

# %% [markdown]
# ### 8.3 Manhattan plot
#
# Plot $-\log_{10}(p\text{-value})$ at each position. Higher peaks =
# stronger convergence signal.

# %%
# Replace p = 0 with a small value to avoid log(0)
pvals = results_df['pvalue'].replace(0, 1 / 10001)
neg_log_p = -np.log10(pvals)

fig, axes = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

# Top panel: entropy (conservation)
axes[0].plot(range(n_positions), entropies, linewidth=0.5, color='steelblue')
axes[0].set_ylabel('Shannon entropy\n(bits)')
axes[0].set_title('Prestin (SLC26A5) — conservation vs. convergence')

# Bottom panel: convergence signal
axes[1].scatter(range(n_positions), neg_log_p, s=4, color='coral', alpha=0.7)
axes[1].axhline(-np.log10(0.05), color='gray', linewidth=1, linestyle='--',
                label='p = 0.05')
axes[1].axhline(-np.log10(0.01), color='gray', linewidth=1, linestyle=':',
                label='p = 0.01')
axes[1].set_xlabel('Alignment position')
axes[1].set_ylabel('$-\\log_{10}$(p-value)')
axes[1].legend()

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 8.4 The top hits

# %%
# Sort by p-value: most significant positions first
top_hits = results_df.sort_values('pvalue').head(20)

print(f"{'Position':>10s}  {'Agreement':>10s}  {'P-value':>10s}  {'Echolocator AAs'}")
print('-' * 70)
for _, row in top_hits.iterrows():
    pos = int(row['position'])
    echo_aas = ''.join(echo_aln[pos].values)
    print(f"  {pos:>8d}  {row['agreement']:>10.3f}  {row['pvalue']:>10.4f}  {echo_aas}")

# %% [markdown]
# ### ✏️ Exercise 6
#
# 1. How many positions pass the p < 0.05 threshold? But we tested
#    hundreds of positions — by chance alone, we'd expect 5% to be
#    "significant." How many false positives would you expect?
#
# 2. **Bonferroni correction:** A simple (conservative) fix is to
#    divide the threshold by the number of tests:
#    ```python
#    bonferroni_threshold = 0.05 / n_positions
#    n_bonferroni = (results_df['pvalue'] < bonferroni_threshold).sum()
#    ```
#    How many positions survive this correction?
#
# 3. Look at the top hits. At those positions, do the echolocating
#    **bats** and the echolocating **cetaceans** share the same amino
#    acid? (That would be true convergence — independent lineages
#    arriving at the same solution.)

# %%
# Your code here


# %% [markdown]
# ---
# ## 9. Discussion and wrap-up
#
# ### What we did
# We built a complete analysis pipeline:
# 1. Loaded a prestin alignment → pandas DataFrame
# 2. Computed Shannon entropy to find conserved regions
# 3. Learned what permutation tests are and how they generate p-values
# 4. Applied a convergence test to every alignment position
# 5. Identified positions where echolocators agree more than expected
#
# ### What we found
# Some positions show a convergence signal — echolocators share the same
# amino acid more than random same-sized groups would. This is consistent
# with the findings of [Parker et al. (2013)](https://www.nature.com/articles/nature12511),
# who showed genome-wide convergent evolution in echolocating mammals.
#
# ### What a rigorous analysis would add
# Our test is a simplified version. A full analysis would include:
# - **Phylogenetic correction** — closely related species share amino
#   acids by inheritance, not convergence. A proper test would account
#   for the species tree.
# - **Ancestral state reconstruction** — to distinguish convergence
#   (independent gains) from retention of an ancestral state.
# - **Multiple testing correction** — we discussed Bonferroni, but
#   methods like FDR (Benjamini-Hochberg) are less conservative.
# - **Domain mapping** — are the convergent sites in functionally
#   important protein domains?
#
# ### The key conceptual point
# Convergent evolution in prestin operates at **individual amino acid
# positions**, not at the level of whole-tree topology. That's why the
# prestin tree may or may not cluster echolocators together — but
# alignment-level analysis reveals the signal.

# %% [markdown]
# ---
# ## 10. What's next
#
# In the **assignment notebook**, you'll apply these same techniques to
# a **control subfamily** — a different SLC26 gene that is NOT involved
# in hearing. If our convergence test is working correctly, the control
# gene should show **no convergence signal** among echolocators.
#
# This is how science works: you need a **negative control** to make
# sure your method isn't just finding noise.
