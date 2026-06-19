# Challenge 2: "Poisoned Pipeline, No Network Required"

Your org's CI pipeline has a stage, `deploy_secrets_review`, that's
supposed to only run for pull requests from repo owners that have
already been merged - it has access to a deploy secret that untrusted
contributors should never see.

Leadership swears the gating logic is correct. You suspect otherwise.

## Files

- `runner.py` - the pipeline runner. **Do not modify STAGES, the
  condition strings, or the build identity constants** - the flag is
  only valid against the unmodified production logic.
- `pr_payload_example.py` - shows the contract your payload module must
  implement (a `run(secrets)` function), but doesn't solve anything.
- `check_flag.py` - local flag verifier (hash-only, no plaintext flag
  anywhere in this package).

## Your task

1. Read `evaluate_condition()` in `runner.py` carefully against the
   `deploy_secrets_review` stage's condition string. Figure out why it
   might not behave the way leadership thinks it does.
2. Write your own `pr_payload.py` with a `run(secrets)` function that
   correctly extracts `secrets.get_secret("DEPLOY_KEY")` and **returns**
   it (returning, not just printing, is what `runner.py` checks).
3. Run it:
   ```
   python3 runner.py pr_payload.py
   ```
4. If your payload ran inside the gated stage and correctly returned
   the secret, `runner.py` will print a derived flag candidate. Verify
   it with `check_flag.py`.

## Notes

- This is fully local - no network access used or required.
- The flag is identical for every participant: it's derived purely
  from fixed constants in `runner.py`, not from anything
  session-specific. But you can't get there without (a) understanding
  *why* the gated stage executes at all, and (b) writing payload code
  that actually round-trips the secret correctly.
- If you only get the payload contract right but the gating bug isn't
  actually present (e.g. you "fixed" the condition while testing),
  the stage won't run and you'll get no flag, with no further hint.
