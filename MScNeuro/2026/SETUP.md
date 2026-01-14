# Setup Instructions

## Step 1: Install Miniconda (in WSL/Ubuntu)

Open your WSL terminal (Ubuntu) and run:

```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Run the installer
bash Miniconda3-latest-Linux-x86_64.sh
```

During installation:
- Press `Enter` to review the license, then type `yes` to accept
- Press `Enter` to confirm the installation location
- Type `yes` when asked to initialize conda

After installation, **close and reopen your terminal**, or run:
```bash
source ~/.bashrc
```

Verify installation:
```bash
conda --version
```

---

## Step 2: Create a Conda Environment

```bash
# Create a new environment named 'neuro105' with Python 3.10
conda create -n neuro105 python=3.10

# Activate the environment
conda activate neuro105
```

You should see `(neuro105)` at the beginning of your terminal prompt.

---

## Step 3: Install Required Packages

With the environment activated, install the packages:

```bash
pip install numpy scipy matplotlib seaborn pandas jupyter
```

---

## Step 4: Run Jupyter Notebook

### Option A: Classic Jupyter Notebook

```bash
# Make sure your environment is activated
conda activate neuro105

# Start Jupyter Notebook
jupyter notebook
```

This will open a browser window. If it doesn't open automatically, copy the URL shown in the terminal (starts with `http://localhost:8888/...`).

### Option B: Using VS Code (Recommended)

1. Open VS Code
2. Install the **Python** extension (if not installed)
3. Install the **Jupyter** extension (if not installed)
4. Open your `.ipynb` file
5. Select kernel: Click on "Select Kernel" (top right) → Choose `neuro105`

---

## Quick Reference

### Activate environment (do this every time)
```bash
conda activate neuro105
```

### Deactivate environment
```bash
conda deactivate
```

### List your environments
```bash
conda env list
```

### Install additional packages
```bash
pip install package_name
```

---

## Troubleshooting

### "conda: command not found"
Close and reopen your terminal, or run:
```bash
source ~/.bashrc
```

### Jupyter doesn't open in browser
Copy the URL from the terminal (looks like `http://localhost:8888/?token=...`) and paste it in your browser.

### Wrong Python version in VS Code
Click on the Python version in the bottom status bar and select the interpreter from your `neuro105` environment.

---

## Useful Links

- [Miniconda Installation](https://docs.conda.io/en/latest/miniconda.html)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)
- [Jupyter in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
