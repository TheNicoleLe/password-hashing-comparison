# Password Hashing Timing Demo

This repository contains a small Python experiment to compare the **average hashing time** of:

- `SHA-256` (fast baseline, **not** suitable for password storage)
- `bcrypt`
- `scrypt`
- `Argon2id` (modern recommended password hashing function)

The goal is to show **how slow, configurable, and memory-hungry password hashing functions are in practice**, and to provide data you can include in your presentation (tables/plots and a short discussion).

---

## Files

- `password_timing_demo.py`  
  Main script that runs the timing experiment and prints average time per hash for each algorithm.

---

## Requirements

- Python 3.8+ (3.10+ recommended)
- `pip` for installing dependencies

Python packages:

- `bcrypt`
- `argon2-cffi`

The standard library modules used are: `time`, `os`, and `hashlib` (no extra install needed for those).

---

## Installation

1. **Clone or copy** the project files to your machine.

2. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
