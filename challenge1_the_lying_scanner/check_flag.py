"""
check_flag.py

Verifies your derived flag locally WITHOUT ever storing or revealing the
real flag in this file. Only a SHA256 hash of the correct flag is
embedded below.

Usage:
    python3 check_flag.py "FLAG{...}"
"""

import hashlib
import sys

# SHA256 of the correct flag. The real flag is never written anywhere
# in this challenge package.
EXPECTED_HASH = "aec3f2c0334162b49c9c782e175c84ba15e5fa02170ebeaf78638f9471225b94"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_flag.py \"FLAG{...}\"")
        sys.exit(1)

    candidate = sys.argv[1].strip()
    candidate_hash = hashlib.sha256(candidate.encode()).hexdigest()

    if candidate_hash == EXPECTED_HASH:
        print("Correct! That is the flag.")
    else:
        print("Not correct. Keep auditing scorer.py against SPEC.md / CHANGELOG.md.")


if __name__ == "__main__":
    main()
