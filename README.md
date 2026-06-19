# CI/CD Risk Prioritization CTF — 3 Challenges

All challenges run fully locally (no network required). Each has
exactly one flag, identical for every participant, derived only after
correctly exploiting/reimplementing the intended vulnerable logic.
No flag is ever stored as plaintext in any shipped file.

## Challenge 1 — The Lying Scanner
`challenge1_the_lying_scanner/`
Fix 3 disguised bugs in a vulnerability-risk-scoring engine to recover
the true top-5 risk ranking. Flag = sha256 of the correctly ranked
finding IDs.

## Challenge 2 — Poisoned Pipeline, No Network Required
`challenge2_poisoned_pipeline/`
Find a Poisoned Pipeline Execution (PPE) condition-evaluator bug that
lets an "untrusted" pipeline stage run unconditionally, then write a
payload that correctly extracts a deploy secret from the live
in-memory secrets context during that stage.

## Challenge 3 — Supply Chain Forge
`challenge3_supply_chain_forge/`
Exploit a broken (prefix-based) signature comparison to forge a valid
artifact signature one character at a time without ever knowing the
real signing key, then pass full verification to trigger deploy.

## Running each challenge

```
cd challengeN_xxx
python3 runner.py        # or verify.py-based workflow per its README
python3 check_flag.py "FLAG{...}"
```

Each challenge folder has its own `README.md` with full instructions.

## For instructors

The `instructor/` package mirrors this structure with a `SOLUTION.md`
per challenge containing the bug writeup, canonical flag, and the
SHA256 hash embedded in the corresponding `check_flag.py`. Use these to
regression-test the participant package stays solvable after any edits
(re-run the solver snippets in each SOLUTION.md and confirm the flag
matches before redistributing).

## All the Best
