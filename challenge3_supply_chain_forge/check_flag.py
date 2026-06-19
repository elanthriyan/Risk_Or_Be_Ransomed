"""
check_flag.py
Usage: python3 check_flag.py "FLAG{...}"
"""
import hashlib
import sys

EXPECTED_HASH = "f5fa1b4c3a61b5a23c3665bea16d766f488ddada0d4603f581107b263327f81c"


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 check_flag.py "FLAG{...}"')
        sys.exit(1)
    candidate = sys.argv[1].strip()
    if hashlib.sha256(candidate.encode()).hexdigest() == EXPECTED_HASH:
        print("Correct! That is the flag.")
    else:
        print("Not correct. Re-check your forged signature and artifact bytes.")


if __name__ == "__main__":
    main()
