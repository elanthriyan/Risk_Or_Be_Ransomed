"""
check_flag.py
Usage: python3 check_flag.py "FLAG{...}"
"""
import hashlib
import sys

EXPECTED_HASH = "873e23f2a40e39f1344b5c0490fe5c5a3cd84121b279fead2f397178c8e2ed76"


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 check_flag.py "FLAG{...}"')
        sys.exit(1)
    candidate = sys.argv[1].strip()
    if hashlib.sha256(candidate.encode()).hexdigest() == EXPECTED_HASH:
        print("Correct! That is the flag.")
    else:
        print("Not correct. Re-check your payload and which stage executed it.")


if __name__ == "__main__":
    main()
