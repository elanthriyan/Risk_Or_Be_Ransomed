"""
runner.py

Loads the fixed findings dataset, runs it through scorer.py, prints the
ranked top 5, and derives a flag from that ranking.

Usage:
    python3 runner.py
"""

import hashlib
from findings_data import generate_findings
from scorer import rank


def derive_flag(top5_ids):
    joined = ",".join(top5_ids)
    digest = hashlib.sha256(joined.encode()).hexdigest()[:32]
    return f"FLAG{{{digest}}}"


def main():
    findings = generate_findings()
    ranked = rank(findings)

    print("Top 10 ranked findings (by your scorer.py):")
    for fid, s in ranked[:10]:
        print(f"  {fid}  score={s}")

    top5_ids = [fid for fid, _ in ranked[:5]]
    flag = derive_flag(top5_ids)
    print()
    print("Derived flag candidate:", flag)
    print()
    print("Run check_flag.py to verify whether this is correct.")


if __name__ == "__main__":
    main()
