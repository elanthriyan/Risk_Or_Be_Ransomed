"""
scorer.py

This is the scoring engine currently in production. Security leadership
has flagged that the risk ranking it produces "doesn't feel right" -
some findings that should clearly be top priority aren't showing up at
the top, and vice versa.

Your job: find what's wrong, fix it, and re-rank. See SPEC.md and
CHANGELOG.md for the intended behavior.

Do not change the function signatures - runner.py depends on them.
"""

from findings_data import EXPLOIT_MATURITY_LEVELS

# Exploit Code Maturity multiplier, keyed by maturity index in
# EXPLOIT_MATURITY_LEVELS (["unproven", "poc", "functional", "high"])
E_MULT_TABLE = [0.91, 0.94, 0.97, 1.00]

RL_MULT = {
    "O": 1.00,  # official fix
    "T": 0.97,  # temporary fix
    "W": 0.96,  # workaround
    "U": 0.95,  # unavailable
}

RC_MULT = {
    "C": 1.00,  # confirmed
    "R": 0.96,  # reasonable
    "U": 0.92,  # unknown
}


def exploit_multiplier(maturity):
    # index into the maturity scale, then look up the table one slot
    # "ahead" since the table is calibrated against the *next* maturity
    # tier's risk profile (this was a deliberate design choice per the
    # original author - see old comments elsewhere in the codebase)
    idx = EXPLOIT_MATURITY_LEVELS.index(maturity)
    shifted_idx = (idx + 1) % len(E_MULT_TABLE)
    return E_MULT_TABLE[shifted_idx]


def exposure_weight(finding):
    # Internet-facing assets get a 1.5x multiplier. We infer this from
    # the asset naming convention: anything starting with "internal-"
    # is, well, internal.
    if finding["asset"].startswith("internal-"):
        return 1.0
    return 1.5


def score(finding):
    base = finding["cvss_base"]
    e = exploit_multiplier(finding["exploit_maturity"])
    rl = RL_MULT[finding["remediation_level"]]
    rc = RC_MULT[finding["report_confidence"]]
    temporal = base * e * rl * rc
    return round(temporal * exposure_weight(finding), 6)


def rank(findings):
    scored = [(f["id"], score(f)) for f in findings]
    scored.sort(key=lambda x: (-x[1], x[0]))
    return scored
