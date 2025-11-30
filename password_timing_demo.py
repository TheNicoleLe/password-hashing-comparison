"""
password_timing_demo.py

Small experiment to compare average hashing time of:
- SHA-256     (fast baseline, NOT for password storage)
- bcrypt
- scrypt
- Argon2id    (modern recommended password hash)

Usage:
    pip install bcrypt argon2-cffi
    python password_timing_demo.py
"""

import time
import os
import hashlib

import bcrypt
from argon2.low_level import hash_secret, Type


# -----------------------------
# Configuration
# -----------------------------

# Test password (bytes)
PASSWORD = b"correct horse battery staple"

# Number of times to repeat each hash for timing
REPEAT = 100

# bcrypt cost (log2 number of rounds)
BCRYPT_COST = 12

# scrypt parameters (roughly "moderate")
SCRYPT_N = 2 ** 14   # CPU/memory cost
SCRYPT_R = 8         # block size
SCRYPT_P = 1         # parallelization

# Argon2id parameters (example; tune for your machine)
ARGON2_TIME_COST = 2       # number of passes over memory
ARGON2_MEMORY_COST = 64_000  # in KiB (64 MiB)
ARGON2_PARALLELISM = 1     # number of lanes


# -----------------------------
# Helper: timing function
# -----------------------------

def time_hasher(name, hash_func, repeat=REPEAT):
    """
    Run hash_func() 'repeat' times and print average time per call in ms.
    hash_func should take no arguments and perform ONE hash.
    """
    start = time.perf_counter()
    for _ in range(repeat):
        hash_func()
    end = time.perf_counter()

    total_seconds = end - start
    avg_ms = (total_seconds / repeat) * 1000.0
    print(f"{name:10s}  {avg_ms:8.2f} ms per hash (over {repeat} runs)")


# -----------------------------
# Hash function wrappers
# -----------------------------

def make_sha256_hasher(password: bytes):
    # No salt here; this is just a FAST baseline
    def do_hash():
        hashlib.sha256(password).hexdigest()
    return do_hash


def make_bcrypt_hasher(password: bytes, cost: int):
    # In a real system, salt is stored per user; here we reuse one salt
    salt = bcrypt.gensalt(rounds=cost)

    def do_hash():
        bcrypt.hashpw(password, salt)
    return do_hash


def make_scrypt_hasher(password: bytes, n: int, r: int, p: int):
    # Random salt; reused for all repetitions (like a real stored hash)
    salt = os.urandom(16)

    def do_hash():
        hashlib.scrypt(password, salt=salt, n=n, r=r, p=p)
    return do_hash


def make_argon2id_hasher(password: bytes,
                         time_cost: int,
                         memory_cost: int,
                         parallelism: int):
    # Random salt; reused for all repetitions
    salt = os.urandom(16)

    def do_hash():
        # hash_len=32 gives a 32-byte output
        hash_secret(
            secret=password,
            salt=salt,
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=32,
            type=Type.ID,   # Argon2id
        )
    return do_hash


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    print("Password hashing timing demo\n")
    print(f"Password: {PASSWORD!r}")
    print(f"Repetitions per algorithm: {REPEAT}")
    print()

    print("Parameters used:")
    print(f"- bcrypt:  cost={BCRYPT_COST}")
    print(f"- scrypt:  N={SCRYPT_N}, r={SCRYPT_R}, p={SCRYPT_P}")
    print(f"- Argon2id: time_cost={ARGON2_TIME_COST}, "
          f"memory_cost={ARGON2_MEMORY_COST} KiB, "
          f"parallelism={ARGON2_PARALLELISM}")
    print()

    # Create hasher callables
    sha256_hasher = make_sha256_hasher(PASSWORD)
    bcrypt_hasher = make_bcrypt_hasher(PASSWORD, BCRYPT_COST)
    scrypt_hasher = make_scrypt_hasher(PASSWORD, SCRYPT_N, SCRYPT_R, SCRYPT_P)
    argon2id_hasher = make_argon2id_hasher(
        PASSWORD,
        ARGON2_TIME_COST,
        ARGON2_MEMORY_COST,
        ARGON2_PARALLELISM,
    )

    # Run timings
    print("Average time per hash:\n")
    time_hasher("SHA-256", sha256_hasher)
    time_hasher("bcrypt", bcrypt_hasher)
    time_hasher("scrypt", scrypt_hasher)
    time_hasher("Argon2id", argon2id_hasher)
