# Challenge: "The Lying Scanner"

Your org's vulnerability scanner aggregates findings from across the
CI/CD pipeline and produces a risk-prioritized list. Leadership has
noticed the rankings look off — low-risk findings are sometimes
outranking ones that should obviously be fixed first.

You've been handed the scoring engine (`scorer.py`) and the raw
findings dataset (`findings_data.py`, do not modify). Something in the
scoring logic is wrong. Multiple somethings, in fact.

## Your task

1. Read `SPEC.md` for the intended scoring behavior.
2. Read `CHANGELOG.md` — it has fragments of the correct historical
   logic buried in old commit messages.
3. Audit `scorer.py` against the spec. Fix what's wrong.
4. Run `python3 runner.py` to see your scorer's top-10 ranking and a
   derived flag candidate.
5. Run `python3 check_flag.py "FLAG{...}"` to verify.

## Rules

- Do not modify `findings_data.py` — the dataset must stay exactly as
  shipped, or your derived flag will never match.
- You may rewrite as much of `scorer.py` as you need to, as long as
  `rank(findings)` still returns a list of `(id, score)` tuples sorted
  correctly.
- There is more than one bug. Fixing only one or two will produce a
  plausible-looking but still-wrong ranking, and a wrong flag, with no
  error message telling you which bug(s) remain. Be rigorous.
- The flag is identical for everyone — it's derived purely from the
  fixed dataset and the *correct* scoring algorithm, not from anything
  random or session-specific.
