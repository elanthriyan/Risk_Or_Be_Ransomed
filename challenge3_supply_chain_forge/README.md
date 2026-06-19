# Challenge 3: "Supply Chain Forge"

Before any artifact can deploy, it must pass `verify.py`'s
`verify_signature(artifact_bytes, candidate_sig)` check. The signing
key is never exposed - it lives only inside a closure in `verify.py`
and cannot be read directly. `verify_signature()` is a black box: you
give it bytes + a candidate signature string, it tells you True/False.

You do not have the signing key. You don't need it.

## Files

- `verify.py` - the verification + deploy gate. **Do not modify this
  file** - your flag depends on its exact, unmodified behavior. You
  may freely *import and call* `verify_signature()` as many times as
  you like, locally, with no rate limit.
- `check_flag.py` - local flag verifier (hash-only).

## Your task

1. The required artifact payload is fixed: `verify.REQUIRED_ARTIFACT`
   (already defined in `verify.py` - don't change it).
2. `verify_signature()` is not doing a real constant-time equality
   check. Figure out what comparison it's actually doing, and what
   that lets you do if you can call it an unlimited number of times
   locally.
3. Write a script that uses repeated calls to `verify_signature()` to
   reconstruct a signature that `verify_signature()` accepts.
4. Once you have a full, valid signature (not just a partial one),
   call `verify.deploy(verify.REQUIRED_ARTIFACT, your_signature)`.
   If it's genuinely complete and correct, it will print a flag.
5. Verify with `check_flag.py`.

## Notes

- A signature that gets `verify_signature()` to return `True` is not
  automatically enough - `deploy()` separately checks that what you
  submit is the *full* signature, not merely an accepted partial one.
- The flag is identical for every participant - it's derived
  deterministically from the fixed artifact bytes and the one true
  signature, which only exists if you actually carry out the attack
  correctly end to end.
- Brute-forcing the full signature in one shot (16^64 guesses) is
  infeasible. Think about what information `verify_signature()` leaks
  you on every call, and how to exploit that incrementally.
