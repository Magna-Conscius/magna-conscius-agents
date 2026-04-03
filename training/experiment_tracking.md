# Experiment Tracking

## Purpose
Experiments must produce memory.
This document defines how results from Colab, simulations, and applied tests are recorded.

## Track For Every Experiment
- experiment name
- date
- model tested
- dataset used
- version of data
- variables changed
- metric or metrics
- expected result
- actual result
- prediction error
- interpretation
- next action

## Tracking Options

### Lightweight
Use markdown records in `Experiments/` plus metric tables in the repository.

Best for:
- very early stage
- few experiments
- solo operation

### Structured
Use MLflow or Weights & Biases alongside markdown summaries.

Best for:
- repeated training runs
- many metrics
- artifact comparison

## Recommendation
Start with markdown plus a simple tracker.
Adopt MLflow or Weights & Biases once experiment volume becomes difficult to compare manually.

## Required Rule
No experiment is complete until the result is written back into:
- an experiment record
- a linked model record
- a short summary in documentation if the result affects priorities

## Evaluation Standard
The key question is not only whether the model performed well.
The key question is whether the model reduced uncertainty enough to justify its continued use.
