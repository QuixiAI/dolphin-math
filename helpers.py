import random
import uuid

DELIM = "|"  # Use standard vertical bar delimiter

def step(op, x="", y="", z="", o=""):
    """Formats a step into a delimited string."""
    parts = [op, str(x), str(y), str(z), str(o)]
    while parts and parts[-1] == "":  # trim empties
        parts.pop()
    return DELIM.join(parts)

def jid() -> str:
    """Generates a unique job ID (UUID4 format).

    Drawn from the `random` module rather than os.urandom so that seeded
    dataset builds (-s/--seed) are reproducible byte-for-byte.
    """
    return str(uuid.UUID(int=random.getrandbits(128), version=4))
