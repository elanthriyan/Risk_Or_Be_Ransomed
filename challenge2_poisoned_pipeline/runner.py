"""
runner.py - local mock CI/CD pipeline runner.

This simulates a YAML-style pipeline with conditional stage execution.
No network access is used or required - everything runs locally.

Pipeline stages are defined below exactly as they exist in production.
Do not modify STAGES or the constants in this file - your derived flag
will only match if the dataset/logic stays exactly as shipped.
"""

import hashlib
import importlib.util
import sys

# --- build/runner identity constants (do not modify) ---
BUILD_TAG = "f3a9c1d0"
RUNNER_VERSION = "78b2e5aa"
ENV_FINGERPRINT = "4c910b77"


class SecretsContext:
    """
    Holds secrets available to a pipeline stage. In a real CI system this
    would be scoped per-stage based on declared permissions. Here, any
    code that executes WITHIN the 'deploy_secrets_review' stage gets a
    reference to this object passed to it.
    """

    def __init__(self):
        # the deploy key is assembled from three build identity
        # constants above, combined the same way the real deploy
        # tooling does it (see ops wiki, "key derivation" - not
        # reproduced here, you'll need to work out the right
        # combination by testing).
        combined = bytes.fromhex(BUILD_TAG) + bytes.fromhex(RUNNER_VERSION) + bytes.fromhex(ENV_FINGERPRINT)
        self._deploy_key = hashlib.sha256(combined).hexdigest()

    def get_secret(self, name):
        if name == "DEPLOY_KEY":
            return self._deploy_key
        raise KeyError(f"no such secret: {name}")


def evaluate_condition(cond_str, context):
    """
    Evaluates a pipeline stage's `if:` condition. Supports simple
    three-token equality checks like "branch == 'main'".
    """
    try:
        left, op, right = cond_str.split()
        left_val = context.get(left, left)
        right_val = right.strip("'\"")
        if op == "==":
            return str(left_val) == right_val
        return False
    except Exception:
        # condition didn't parse as a simple equality check - fall back
        # to treating it as a flag string
        return bool(cond_str)


STAGES = [
    {"name": "checkout", "condition": "always == 'true'", "action": "noop"},
    {"name": "install_deps", "condition": "always == 'true'", "action": "noop"},
    {"name": "run_tests", "condition": "always == 'true'", "action": "noop"},
    {
        "name": "deploy_secrets_review",
        # intent: only run for PRs from repo owners that have been merged.
        # DO NOT change this condition string - it must stay exactly as
        # shipped in production for your flag to be valid.
        "condition": "pull_request.author_association == 'OWNER' and pull_request.merged == true",
        "action": "deploy_review",
    },
    {"name": "external_contribution_check", "condition": "is_fork == 'true'", "action": "noop"},
    {"name": "cleanup", "condition": "always == 'true'", "action": "noop"},
]


def run_pipeline(payload_path=None, context=None, verbose=True):
    context = context or {}
    secrets = SecretsContext()
    executed = []
    captured = {}

    for stage in STAGES:
        triggered = evaluate_condition(stage["condition"], context)
        if verbose:
            print(f"[stage] {stage['name']:30s} condition={triggered}")
        if not triggered:
            continue
        executed.append(stage["name"])

        if stage["action"] == "deploy_review" and payload_path:
            spec = importlib.util.spec_from_file_location("pr_payload", payload_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
                result = mod.run(secrets)
                if result:
                    captured["deploy_review_output"] = result

    return executed, captured


def derive_flag(executed_stages, captured_secret):
    """
    Flag only derivable if:
      1. 'deploy_secrets_review' actually executed (the PPE bug was
         triggered), AND
      2. the payload correctly extracted and returned DEPLOY_KEY.
    """
    if "deploy_secrets_review" not in executed_stages:
        return None
    if not captured_secret:
        return None
    expected_secret = SecretsContext().get_secret("DEPLOY_KEY")
    if captured_secret != expected_secret:
        return None
    digest = hashlib.sha256(captured_secret.encode()).hexdigest()[:32]
    return f"FLAG{{{digest}}}"


def main():
    payload_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not payload_path:
        print("Usage: python3 runner.py path/to/pr_payload.py")
        sys.exit(1)

    executed, captured = run_pipeline(payload_path=payload_path)
    print()
    print("Executed stages:", executed)

    flag = derive_flag(executed, captured.get("deploy_review_output"))
    if flag:
        print("Derived flag candidate:", flag)
    else:
        print("No flag derived - either the deploy_secrets_review stage")
        print("did not execute, or your payload didn't correctly return")
        print("the DEPLOY_KEY secret from its run(secrets) function.")


if __name__ == "__main__":
    main()
