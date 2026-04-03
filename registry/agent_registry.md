# Agent Registry

## Purpose
This file defines the initial agent system for Magna Conscius.
Agents must have narrow scopes, explicit inputs, and review checkpoints.

## Global Rules
- agents assist judgment; they do not replace it
- agents should produce structured outputs
- high-impact outputs require human review
- agents must read from documented sources, not hidden assumptions
- prompts and versions should be tracked

## Required Fields
- agent name
- role
- inputs
- outputs
- tools allowed
- write locations
- approval requirement
- evaluation criteria

## Initial Agents

### Agent Name
Research Agent

### Role
Convert questions and observations into structured research notes, source summaries, and candidate hypotheses.

### Inputs
- research question
- relevant notes
- existing models

### Outputs
- research summary
- open questions
- testable hypotheses

### Tools Allowed
- repo documents
- literature notes
- internal datasets

### Write Locations
- `Research/`
- `Documentation/LabNotes/`

### Approval Requirement
Human review before findings are treated as validated.

### Evaluation Criteria
- clarity
- source grounding
- quality of hypotheses

### Agent Name
Model Agent

### Role
Turn hypotheses into formal model drafts with variables, assumptions, mechanisms, and predictions.

### Inputs
- research notes
- prior models
- target prediction problem

### Outputs
- model draft
- variable list
- failure conditions

### Tools Allowed
- repo documents
- model templates

### Write Locations
- `Models/`

### Approval Requirement
Human review before model becomes active.

### Evaluation Criteria
- coherence
- falsifiability
- simplicity

### Agent Name
Experiment Agent

### Role
Design tests for models and define what evidence would strengthen or weaken them.

### Inputs
- model spec
- available data
- target metric

### Outputs
- experiment plan
- variable definitions
- predicted result

### Tools Allowed
- repo documents
- experiment templates
- dataset summaries

### Write Locations
- `Experiments/`
- `Documentation/ExperimentLogs/`

### Approval Requirement
Human review before execution.

### Evaluation Criteria
- testability
- metric quality
- linkage to prediction error

### Agent Name
Insight Agent

### Role
Convert research, experiment, and model outputs into briefs, reports, and decision memos.

### Inputs
- validated findings
- client or product context

### Outputs
- summary memo
- strategic recommendation
- report draft

### Tools Allowed
- repo documents
- approved results

### Write Locations
- `Documentation/`
- `Applications/Products/`

### Approval Requirement
Human review before external delivery.

### Evaluation Criteria
- actionability
- accuracy
- compression quality

### Agent Name
Ops Agent

### Role
Maintain roadmap hygiene, log open work, and keep initiative status visible.

### Inputs
- current projects
- decision records
- execution status

### Outputs
- roadmap updates
- status summaries
- missing dependency alerts

### Tools Allowed
- roadmap docs
- decision logs
- registries

### Write Locations
- `Documentation/`

### Approval Requirement
Human review for major prioritization changes.

### Evaluation Criteria
- accuracy
- completeness
- operational usefulness

## Initial Recommendation
Start with three agents first:
- research agent
- model agent
- insight agent

Add experiment and ops agents after the first workflow is stable.
