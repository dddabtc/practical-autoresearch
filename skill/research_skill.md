# Research Skill (Public Playbook Artifact)

A reusable skill-style blueprint for running iterative research loops.

Top-level inspiration: Karpathy-style autoresearch.

This public version does **not** assume any private project, benchmark, hardware endpoint, model provider, or company-specific design constraints.

## Trigger
Use when running repeated experiment-analysis-decision cycles on an ML, AI, retrieval, agent, or systems problem.

## Inputs
- problem statement
- current baseline and metrics
- time / compute / cost budget
- constraints (latency, safety, legal, infra, reproducibility)

## Procedure
1. validate baseline
2. select next hypothesis
3. make a controlled change
4. run evaluation
5. analyze deeply
6. apply acceptance gate
7. update ledger and status files
8. scan new papers / repos / reports
9. queue the next experiment

## Outputs
- updated ledger entry
- round log
- current status snapshot
- ranked next experiments
- external research intake note (when relevant)

## Quality bar
- reproducible configs
- evidence-linked decisions
- explicit uncertainty
- durable resumable state
- no acceptance without clear reasoning
