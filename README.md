# practical-autoresearch

**A practical playbook for running evidence-driven autoresearch loops.**

Inspired by the high-level logic of Karpathy's autoresearch, but optimized for real-world use:

- stronger baseline discipline
- deeper post-run analysis
- explicit acceptance gates
- durable file-based state
- controlled paper / repo / SOTA intake
- reusable templates for repeated experiment loops

---

## TL;DR

Most research loops fail for boring reasons:

- the baseline was unstable,
- too many things changed at once,
- the evaluation path drifted,
- a weak proxy metric was mistaken for real progress,
- or the whole loop depended on a transient chat/session.

**practical-autoresearch** is a small public repo that tries to fix that.

It gives you a reusable operating pattern for iterative research work on:

- ML systems
- retrieval systems
- agent systems
- evaluation pipelines
- benchmark optimization loops
- any setup where repeated experiment → analysis → next-step cycles matter

---

## Short intro

`practical-autoresearch` is a public methodology repo for running automatic research loops with stronger rigor: baseline-first, evidence-driven, resumable, and designed for real engineering constraints.

---

## What makes this different

Karpathy-style autoresearch gives the top-level spirit:

- iterate fast
- measure tightly
- keep the loop autonomous where possible

This repo adds the practical layer that many teams end up needing anyway:

### 1. Baseline is sacred
If the baseline is not trustworthy, all downstream conclusions are suspect.

### 2. Deep analysis is mandatory
A round does not end at “metric up”. It ends when you understand:
- what improved,
- what regressed,
- which slices moved,
- how strong the signal is,
- and what the next best move should be.

### 3. Acceptance gates beat self-deception
Fast local evaluation is useful. It is not enough for important acceptance decisions.

### 4. Research should survive resets
A serious loop should be resumable from files, not dependent on one agent session or one person's memory.

### 5. New papers enter through controlled intake
This repo encourages continuous scanning of papers, repos, and system reports — but only through explicit evaluation, not novelty impulse.

---

## What this repo contains

```text
.
├── README.md
├── LICENSE
├── SKILL.md
├── docs/
│   ├── methodology.md
│   ├── acceptance-gates.md
│   ├── experiment-ledger-spec.md
│   └── research-program-template.md
├── research-loop/
│   └── templates/
│       ├── round-log.md
│       └── post-run-analysis.md
└── skill/
    ├── autoresearch-playbook/
    │   └── SKILL.md
    └── research_skill.md
```

---

## Core operating model

A healthy autoresearch loop usually looks like this:

1. define objective, constraints, and success metric
2. verify a trustworthy baseline
3. run one focused experiment round
4. analyze deeply
5. apply an acceptance gate
6. scan external developments
7. decide the next move from evidence
8. update durable state files

In short:

> **establish truth → test carefully → analyze deeply → update direction → preserve state → repeat**

---

## Recommended durable files

For a real project, keep the loop state in files like these:

```text
my-autoresearch-worktree/
├── program.md
├── ledger.jsonl
├── CURRENT_STATUS.md
├── experiments/
│   └── NNN/
│       ├── round-log.md
│       └── diff.patch
├── eval/
│   └── eval_harness.py
└── src/
    └── ... system under test ...
```

### Suggested roles

- `program.md` — goals, constraints, active hypotheses, queue
- `ledger.jsonl` — append-only experiment history
- `CURRENT_STATUS.md` — resumable snapshot for humans/agents
- `experiments/NNN/` — detailed per-round logs and diffs
- `eval_harness.py` — as stable as possible across rounds
- `src/` — the thing being improved

---

## Documentation map

- **Methodology** → [`docs/methodology.md`](docs/methodology.md)
- **Acceptance gates** → [`docs/acceptance-gates.md`](docs/acceptance-gates.md)
- **Experiment ledger spec** → [`docs/experiment-ledger-spec.md`](docs/experiment-ledger-spec.md)
- **Research program template** → [`docs/research-program-template.md`](docs/research-program-template.md)
- **Round log template** → [`research-loop/templates/round-log.md`](research-loop/templates/round-log.md)
- **Post-run analysis template** → [`research-loop/templates/post-run-analysis.md`](research-loop/templates/post-run-analysis.md)
- **Skill-style reusable prompt** → [`SKILL.md`](SKILL.md)

---

## Good fit for

This repo is especially useful for people working on:

- retrieval and memory systems
- agent evaluation loops
- benchmark optimization programs
- model routing / tool-use systems
- production ML systems where regressions are expensive
- any experimental stack that needs repeated, explainable iteration

---

## Not this repo's goal

This repo is **not**:

- a benchmark leaderboard
- a dump of private experiments
- a claim of implementation parity with any other repo
- tied to a single dataset, company, model provider, or hardware setup

It is meant to stay public, reusable, and method-oriented.

---

## Why the name

The point is not “fully autonomous research theater”.
The point is **practical autoresearch**:

- good enough to run in the real world,
- disciplined enough to avoid fake progress,
- simple enough to reuse across projects.

---

## License

[MIT](LICENSE)
