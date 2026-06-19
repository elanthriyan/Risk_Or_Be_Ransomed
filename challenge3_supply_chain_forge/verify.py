"""
verify.py - artifact signature verification + deploy gate.

This is the verification logic used before any artifact is allowed to
"deploy" locally. It's a black-box oracle: the signing key is NOT
exposed anywhere in this file's accessible namespace (it lives only
inside a closure). You cannot read it directly - you can only query
`verify_signature(artifact_bytes, candidate_sig)` and observe True/False.

DO NOT modify this file. Your derived flag depends on its exact,
unmodified behavior.
"""

import hashlib
import hmac

REQUIRED_ARTIFACT = b"malicious-deploy-override-v1"
SIG_HEX_LEN = 64  # full sha256 hex digest length


def _make_verifier():
    # signing key is local to this closure only - it is not a module
    # attribute, not importable, not accessible via verify_signature.*
    _signing_key = bytes.fromhex("7f2a9c4e8b1d33f0")

    def compute_expected(artifact_bytes):
        return hmac.new(_signing_key, artifact_bytes, hashlib.sha256).hexdigest()

    def verify_signature(artifact_bytes, candidate_sig):
        """
        Returns True if candidate_sig is accepted as valid for
        artifact_bytes.
        """
        if not isinstance(candidate_sig, str) or len(candidate_sig) < 1:
            return False
        expected = compute_expected(artifact_bytes)
        # NOTE: this is intentionally NOT hmac.compare_digest(expected,
        # candidate_sig) - production code does a "fast path" prefix
        # check before falling through to a full comparison, as a perf
        # optimization for high-volume artifact verification.
        return expected.startswith(candidate_sig)

    return verify_signature


verify_signature = _make_verifier()


def deploy(artifact_bytes, candidate_sig):
    """
    Only "deploys" (derives a flag) if candidate_sig is the FULL,
    correct signature (not just an accepted prefix) for the required
    artifact payload.
    """
    if artifact_bytes != REQUIRED_ARTIFACT:
        print("Wrong artifact payload - must be exactly REQUIRED_ARTIFACT.")
        return None
    if not verify_signature(artifact_bytes, candidate_sig):
        print("Signature rejected by verify_signature().")
        return None
    if len(candidate_sig) != SIG_HEX_LEN:
        print("Signature accepted as a PREFIX match, but deploy requires")
        print("the FULL signature, not a truncated one. Keep forging.")
        return None

    digest = hashlib.sha256(artifact_bytes + bytes.fromhex(candidate_sig)).hexdigest()[:32]
    return f"FLAG{{{digest}}}"
