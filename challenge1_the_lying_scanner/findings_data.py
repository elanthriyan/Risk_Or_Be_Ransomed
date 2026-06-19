"""
findings_data.py
Fixed, deterministic findings dataset shared by every participant.
DO NOT regenerate with a different seed - the dataset must be identical
for all participants so that the final flag is identical for all of them.
"""

import random

SEED = 1337

ASSET_POOL = [
    "internal-gateway-public", "payments-api", "auth-service",
    "internal-billing-db", "edge-cache-01", "internal-reporting-svc",
    "customer-portal", "internal-metrics-public", "build-agent-pool",
    "legacy-admin-panel", "internal-vpn-gateway", "ci-runner-fleet",
    "internal-search-public", "notification-svc", "internal-batch-worker",
]

EXPLOIT_MATURITY_LEVELS = ["unproven", "poc", "functional", "high"]


def generate_findings():
    rng = random.Random(SEED)
    findings = []
    for i in range(1, 51):
        fid = f"FIND-{i:03d}"
        cvss_base = round(rng.uniform(2.0, 9.9), 1)
        maturity = rng.choice(EXPLOIT_MATURITY_LEVELS)
        asset = rng.choice(ASSET_POOL)
        # ground truth exposure - independent of naming, this is what a human
        # asset inventory would say. Scoring code should use THIS to decide
        # exposure weight, not infer it from the asset name.
        internet_facing = rng.random() < 0.35
        # CVSS vector temporal metrics (kept simple: E = exploit maturity,
        # RL = remediation level, RC = report confidence)
        remediation_level = rng.choice(["O", "T", "W", "U"])  # official/temp/workaround/unavailable
        report_confidence = rng.choice(["C", "R", "U"])  # confirmed/reasonable/unknown

        findings.append({
            "id": fid,
            "cvss_base": cvss_base,
            "exploit_maturity": maturity,
            "remediation_level": remediation_level,
            "report_confidence": report_confidence,
            "asset": asset,
            "internet_facing": internet_facing,
        })
    return findings


if __name__ == "__main__":
    for f in generate_findings():
        print(f)
