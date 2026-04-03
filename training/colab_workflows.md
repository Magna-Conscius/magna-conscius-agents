# Colab Workflows

## Purpose
Define how Google Colab should be used inside Magna Conscius so notebooks remain operational, reproducible, and connected to the rest of the organization.

## Why Colab First
- fast startup
- low infrastructure burden
- strong Python support
- accessible GPU options when needed

## Colab Use Cases
- exploratory data analysis
- feature engineering
- baseline model training
- evaluation and comparison
- simulation runs
- report-ready charts and outputs

## Required Notebook Types

### 1. Research Notebook
Use for:
- data inspection
- pattern finding
- quick visual analysis

Output:
- notes that link back to `Research/`

### 2. Training Notebook
Use for:
- building and fitting models
- comparing candidate algorithms

Output:
- metrics, artifacts, and links to `Models/`

### 3. Evaluation Notebook
Use for:
- error analysis
- threshold testing
- bias or stability checks

Output:
- model evaluation summary and links to `Experiments/`

### 4. Simulation Notebook
Use for:
- scenario generation
- Monte Carlo analysis
- parameter sweeps

Output:
- simulation outputs and links to `Simulations/`

## Notebook Rules
- each notebook should solve one clear question
- notebook names should include date and purpose
- notebook outputs should be summarized in markdown files inside the repo
- final metrics should be copied into experiment or model records
- artifact paths should be logged

## Recommended Naming
- `YYYY-MM-DD_research_<topic>.ipynb`
- `YYYY-MM-DD_train_<model>.ipynb`
- `YYYY-MM-DD_eval_<model>.ipynb`
- `YYYY-MM-DD_sim_<scenario>.ipynb`

## Storage Pattern
- code and summaries in repo
- large artifacts in Drive or cloud storage
- references to artifact locations stored in model or experiment docs

## Minimal Colab Setup Checklist
1. mount storage if needed
2. load dataset from cataloged location
3. record dataset version
4. define objective and metric
5. run notebook
6. save artifacts
7. update model and experiment records

## Failure Pattern To Avoid
Colab becomes destructive when notebooks are used as private scratchpads with no registry, no naming discipline, and no summary written back into the repository.
