# Acceptance Gates

A research loop needs explicit rules for when a result should be accepted, rejected, or held for further exploration.

Without acceptance gates, loops drift into self-deception.

---

## 1) Why gates matter

Fast local iteration is valuable, but:

- cheap evaluators can be biased,
- proxy metrics can be misaligned,
- local improvements can hide regressions,
- and headline gains can disappear under stronger validation.

Acceptance gates are how you stop “promising” from being confused with “real”.

---

## 2) Three common outcomes

### ACCEPT
Use when the result:

- improves the primary metric,
- survives slice checks,
- passes the stronger confirmation path,
- and does not violate core design constraints.

### REJECT
Use when the result:

- fails the primary metric threshold,
- regresses important slices,
- breaks constraints,
- or fails stronger confirmation.

### EXPLORE
Use when the result:

- is directionally interesting,
- but signal strength is weak,
- confidence is low,
- or additional controlled variants are needed.

---

## 3) Minimal public gate structure

```text
Fast local validation
        │
        ▼
Does result clear local threshold?
        │
   NO → REJECT
        │
       YES
        │
        ▼
Run stronger confirmation path
        │
        ▼
Does stronger path confirm the gain?
        │
   YES → ACCEPT
   NO  → REJECT or EXPLORE
```

---

## 4) What should be checked before ACCEPT

At minimum:

- primary metric delta
- key slice deltas
- cost / latency impact
- constraint compliance
- robustness / rerun stability
- stronger confirmation result

---

## 5) Example threshold logic

These are examples, not universal defaults:

- local threshold: primary metric >= baseline + 1pp
- confirmation threshold: strong evaluator also >= baseline + 1pp
- regression rule: reject if any critical slice drops > 1pp
- instability rule: reject if reruns vary beyond a defined band

The threshold values should depend on your domain, noise level, and cost of false positives.

---

## 6) Design constraints should outrank score bumps

A result should not be accepted just because the metric went up.

If it violates a non-negotiable design rule, reject it.

Examples of such rules might include:

- recoverability of original evidence
- safety or compliance boundaries
- reproducibility requirements
- latency ceilings
- memory or storage invariants
- explainability / traceability needs

---

## 7) Ledger implications

Every acceptance decision should be written to the ledger with:

- the baseline,
- the measured deltas,
- the evaluator(s) used,
- the decision,
- and the reason.

A future reader should be able to answer:

> Why was this accepted at the time?

without needing the original conversation transcript.
