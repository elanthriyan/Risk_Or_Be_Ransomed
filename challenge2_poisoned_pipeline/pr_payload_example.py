# pr_payload_example.py
#
# This is an EXAMPLE showing the contract runner.py expects from a
# payload module - it does NOT solve the challenge. It's here so you
# know the function signature without having to reverse-engineer
# importlib usage in runner.py.
#
# Your real payload needs to actually retrieve and RETURN the
# DEPLOY_KEY secret string from run(secrets) - this one deliberately
# does not.


def run(secrets):
    print("this payload ran, but doesn't do anything useful yet")
    return None
