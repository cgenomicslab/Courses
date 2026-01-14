# Setup Instructions

## Step 0: Install WSL and Ubuntu (Windows only)

WSL (Windows Subsystem for Linux) lets you run Linux on Windows.

### 0.1 Enable WSL

Open **PowerShell as Administrator** (right-click → "Run as administrator") and run:

```powershell
wsl --install
```

This will:
- Enable WSL
- Install Ubuntu (default Linux distribution)

**Restart your computer** when prompted.

### 0.2 First-time Ubuntu Setup

After restart, Ubuntu will open automatically (or search for "Ubuntu" in Start menu).

You'll be asked to create a username and password:
- Choose a simple username (lowercase, no spaces)
- Choose a password (you won't see it as you type - this is normal)
- Remember this password! You'll need it for `sudo` commands

### 0.3 Update Ubuntu

Run these commands in the Ubuntu terminal:

```bash
sudo apt update
sudo apt upgrade -y
```

### 0.4 (Optional) Install VS Code WSL Extension

If using VS Code:
1. Open VS Code in Windows
2. Install the **WSL** extension
3. Click the green button in the bottom-left corner → "Connect to WSL"

Now you can edit files in WSL directly from VS Code.

---

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

### WSL Issues

**"WSL 2 requires an update to its kernel component"**
Download and install the WSL2 kernel update from:
https://aka.ms/wsl2kernel

**"Virtualization not enabled"**
You need to enable virtualization in your BIOS settings. The exact steps depend on your computer manufacturer.

**Ubuntu not appearing after restart**
Search for "Ubuntu" in the Windows Start menu. If not found, open PowerShell and run:
```powershell
wsl --install -d Ubuntu
```

### Conda Issues

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

- [WSL Installation Guide (Microsoft)](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Miniconda Installation](https://docs.conda.io/en/latest/miniconda.html)
- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)
- [Jupyter in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
