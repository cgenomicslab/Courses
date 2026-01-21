# Introduction to Statistics course (NEURO-105)
* Postgraduate MSc Program in Neurosciences
* University of Crete - [Program Website](https://neurosciences.med.uoc.gr/index.php/el/prog-2)

### Contact
**[Dimitris Tzeranis](mailto:tzeranis@imbb.forth.gr)** | **[Alexandros Pittis](mailto:alexandros.pittis@gmail.com)**

### Room
Computer room, Dept of Biology, UoC

---

## Learning Objectives
- Comprehension of statistical concepts and methods widely used in biomedical research
- Ability to interpret the results of statistical analyses as well as the documented critical evaluation of the statistical methodology of biomedical publications

## Course Content
* Random variables (continuous and discrete)
* The concept of probability, joint probability, conditional probability, Bayes' theorem
* Descriptive statistics (frequency distributions, measures of central tendency)
* Key distributions: Poisson, Bernoulli, Binomial, Uniform, Normal, Student, Chi-square
* Normal distribution: properties and calculations
* Sampling, central limit theorem, confidence region
* Statistical Hypotheses Tests: significance level, p-value, type I & II errors
* Parametric hypothesis tests (z-test, t-test, paired t-test), Analysis of Variance (ANOVA)
* Applications: noise, selecting and applying statistical tests, fitting models to data, estimating variable correlation, dimension reduction, data classification, signal to noise ratio
* Intro to statistics using Python

---

## Schedule

| DATE | TIME | DESCRIPTION | INSTRUCTOR |
| --- | --- | --- | --- |
| Mon 12/1/26 | 1-3pm | Random variables. The concept of probability, joint & conditional probability. Descriptive statistics. | Dimitris Tzeranis |
| Wed 14/1/26 | 3:30-5:30pm | Key distributions and their applications. Normal distribution. Applications: noise, signal processing. | Dimitris Tzeranis |
| **Fri 16/1/26** | **12-2pm** | **Statistics and probability using Python.** | **Alexandros Pittis** |
| Mon 19/1/26 | 12-2pm | Sampling, central limit theorem, confidence regions. Statistical Hypotheses Tests: significance, p-value, errors | Dimitris Tzeranis |
| Wed 21/1/26 | 3:30-5:30pm | Parametric hypothesis tests (z-test, t-test, paired t-test, ANOVA). Selecting and applying statistical tests. | Dimitris Tzeranis |
| **Fri 23/1/26** | **12-2pm** | **Applications: fitting models to data, estimating variable correlation.** | **Alexandros Pittis** |
| **Mon 26/1/26** | **12-2pm** | **Applications: Permutation and non-parametric tests, p-value estimation** | **Alexandros Pittis** |
| **Wed 28/1/26** | **3:30-5:30pm** | **Applications: Hands-on project, case study** | **Alexandros Pittis** |

---

## Lectures

### Python Sessions (Alexandros Pittis)

| Lesson | Topic | Materials |
| --- | --- | --- |
| Lesson 1 (16/1) | Statistics and Probability using Python | [Jupyter Notebook](notebooks/Lesson_1_Intro_to_Statistics_Python.ipynb) |
| Lesson 2 (23/1) | Pandas, Correlation, Regression | [Jupyter Notebook](notebooks/Lesson_2_Correlation_Regression.ipynb) |
| Lesson 3 (26/1) | Permutation tests, p-value estimation | *Coming soon* |
| Lesson 4 (28/1) | Hands-on project | *Coming soon* |

---

## Setup Instructions

👉 **See [SETUP.md](SETUP.md) for detailed installation instructions**

### Easiest: Google Colab (No Installation)

Open notebooks directly in your browser: https://colab.research.google.com

### Local Installation (Quick Start)

```bash
# Create and activate environment
conda create -n neuro105 python=3.10
conda activate neuro105

# Install packages
pip install numpy scipy matplotlib seaborn pandas jupyter

# Run Jupyter
jupyter notebook
```

---

## Resources

### Main References
* [John H. Mcdonald, Handbook Of Biological Statistics. Third Edition](https://www.biostathandbook.com/)
* [Python Statistics Fundamentals: How to Describe Your Data](https://realpython.com/python-statistics/)
* [Quantitative Analysis Guide](https://guides.nyu.edu/quant/python)

### Python & Data Science
* [Pandas Tutorial](https://www.geeksforgeeks.org/pandas/pandas-tutorial/)
* [Non-beginner's python cheat sheet](https://gto76.github.io/python-cheatsheet/)
* [Scientific Python Cheatsheet](https://ipgp.github.io/scientific_python_cheat_sheet/)
* [Matplotlib Cheatsheet](https://matplotlib.org/cheatsheets/)

### Why Jupyter?
* [Why Jupyter is data scientists' computational notebook of choice](https://www.nature.com/articles/d41586-018-07196-1)
* [28 Jupyter Notebook tips, tricks and shortcuts](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)

### SciPy & Statistics
* [SciPy paper in Nature Methods](https://www.nature.com/articles/s41592-019-0686-2) (published: 3 February 2020)
* [SciPy Lectures](http://scipy-lectures.org/)
* [SciPy Statistical Functions Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

### Pandas
* [Introduction to Pandas](https://realpython.com/pandas-dataframe/)
* [Plotting with Pandas](https://realpython.com/pandas-plot-python/)
* [100 pandas puzzles](https://github.com/ajcr/100-pandas-puzzles)
* [Pandas Illustrated: The Definitive Visual Guide to Pandas](https://betterprogramming.pub/pandas-illustrated-the-definitive-visual-guide-to-pandas-c31fa921a43)

### Practice
* [HackerRank Python Challenges](https://www.hackerrank.com/dashboard)

### About Data Science
* [Data Fallacies to Avoid](https://www.geckoboard.com/best-practice/statistical-fallacies/) - Common statistical pitfalls

---

## License
Educational materials for NEURO-105, MSc in Neurosciences, University of Crete.
