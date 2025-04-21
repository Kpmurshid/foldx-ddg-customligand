# FoldX-CustomLigand-DDG

A streamlined workflow for calculating protein stability and ligand-binding ΔΔG values using FoldX, with support for non-standard ligands through PyFoldX-based parameterization.

---

## 🔍 Overview

This repository provides a pipeline to:

- **Parameterize a custom ligand** using PyFoldX.
- **Repair protein-ligand complexes** using FoldX.
- **Introduce mutations** and compute stability ΔΔG values.
- **Analyze protein-ligand binding energies** for each mutant using `AnalyseComplex`.

---

## 📁 Repository Structure

```
.
├── calculate_ddg.py                  # Parses FoldX AnalyseComplex results to calculate ΔΔG values
├── foldx_atom_typing.py             # Custom atom renaming for FoldX compatibility using RDKit Sybyl annotations
├── paramX_AtomNames.ipynb           # Jupyter notebook for ligand parameterization
├── individual_list.txt              # Mutation list for FoldX 
├── complex.pdb                      # Initial protein-ligand complex
├── complex_repaired.pdb             # Repaired structure by FoldX
├── complex_repaired.fxout           # FoldX summary output
├── mutation_ddg_results.csv         # CSV summary of ΔΔG values
├── mutation_ddg_plot.png            # Visual plot of mutation effects
├── run_analyse_complex.sh           # Shell script to automate FoldX AnalyseComplex
├── AnalyseComplex_Results/          # All energy analysis & interaction output files
├── Build_model/                     # Mutant PDB files from FoldX BuildModel
├── paramx_output/ligand_full.pdb    # PyFoldX-generated ligand structure
├── molecules/MFX.json               # Custom ligand parameter file
```

---

## 🧪 Requirements

- Python  3.8+
- [FoldX 5 or 5.1](https://foldxsuite.crg.eu/)
- [PyFoldX](https://github.com/leandroradusky/pyfoldx)
- NumPy, Pandas, Matplotlib (for analysis & plotting)
- RDKit (for ligand atom typing using Sybyl descriptors)

---

## ⚙️ Installation

### Step 1: Install Python Dependencies

```bash
pip install numpy pandas matplotlib
```

**Install RDKit (recommended via conda):**

```bash
conda install -c conda-forge rdkit
```

### Step 2: Install FoldX and PyFoldX

Before starting, a FoldX executable is required for PyFoldX to function. Register and download it here: https://foldxsuite.crg.eu

Then, add FoldX to your `.bashrc`:

```bash
export FOLDX_BINARY=/your/path/to/foldx
```

(Optional) Create a virtual environment:

```bash
virtualenv pyfoldx-env
source pyfoldx-env/bin/activate
```

Install PyFoldX:

```bash
pip install pyfoldx
```

---

## 🧬 rotabase.txt Configuration

PyFoldX requires a `rotabase.txt` file for ligand parameterization.

Edit your `paramx.py` (or wherever you use PyFoldX) and ensure the correct path is set:

```python
# @TODO: make this an option to specify!
ROTABASE_PATH = "/home/foldx5Linux64/rotabase.txt"
```

Make sure this file is placed correctly and accessible before running parameterization.

---

## ⚙️ Usage

### 1. Ligand Parameterization (PyFoldX)

Use `paramX_AtomNames.ipynb` to:

- Generate a custom `.json` file for the ligand.
- Create `ligand_full.pdb` using PyFoldX.
- Atom types are annotated using RDKit with Sybyl descriptors via `foldx_atom_typing.py`. **Manual verification is recommended after auto-mapping.**

### 2. Prepare the Complex

Place your protein-ligand structure in `complex.pdb` and run:

```bash
FoldX --command=RepairPDB --pdb=complex.pdb
```

This generates `complex_repaired.pdb`.

### 3. Introduce Mutations

List your mutations in `individual_list.txt` (WT residue, chain, residue number, mutant residue;) and run:

```bash
FoldX --command=BuildModel --pdb=complex_repaired.pdb --mutant-file=individual_list.txt --numberOfRuns=3
```

Mutant structures will be stored in the `BuildModel/` folder.

### 4. Run AnalyseComplex

To automate running AnalyseComplex for all mutants, use:

```bash
bash run_analysecomplex.sh
```

This will iterate through all repaired mutant PDBs (`complex_repaired_*.pdb`) and save interaction outputs in `AnalyseComplex_Results/`.

**Make sure your script looks like this:**

```bash
#!/bin/bash
mkdir -p AnalyseComplex_Results
for pdb in complex_repaired_*.pdb; do
    FoldX --command=AnalyseComplex --pdb=$pdb --analyseComplexChains=A,L
    mv Interaction_Complex_* AnalyseComplex_Results/
    mv *.fxout AnalyseComplex_Results/
done
```

> You can edit `analyseComplexChains=A,B` if your chains are different.

### 5. Calculate Binding & Stability ΔΔG

After running `AnalyseComplex`, analyze the results using:

```bash
python calculate_ddg.py
```

This will:

- Parse FoldX output energy files.
- Compute ligand binding ΔΔG and overall protein stability changes.
- Save results in `mutation_ddg_results.csv`.
- Generate a plot of mutation effects (`mutation_ddg_plot.png`).

---

## 📊 Output

- CSV file of ΔΔG values: `mutation_ddg_results.csv`
- Energy terms from `AnalyseComplex` in `AnalyseComplex_Results/`
- Visualization of mutation effects: `mutation_ddg_plot.png`

---

## 📌 Notes

- Atom mapping in `foldx_atom_mapping.py` uses RDKit's Sybyl atom type annotations.
- Always **manually verify** atom type mappings and PyFoldX JSON parameters.
- This pipeline allows ligand-specific FoldX-compatible mutation energy profiling.

---

## 📜 License

MIT License

---

## 🤝 Acknowledgements

- This ongoing project is being supported by Telscie Genetics Pvt Ltd
- [FoldX Suite](https://foldxsuite.crg.eu/)
- [PyFoldX by Leandro Radusky](https://github.com/leandroradusky/pyfoldx)

---

