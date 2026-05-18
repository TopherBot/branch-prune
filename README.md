# branch-prune

A one‑file Python utility to clean up merged local Git branches.

## Features
- Show merged branches
- Delete them with a single flag
- No external dependencies (uses only the standard library)

## Installation
```bash
curl -sSL https://raw.githubusercontent.com/yourname/branch-prune/main/branch_prune.py -o branch_prune.py
chmod +x branch_prune.py
```

## Usage
```bash
# Dry‑run: list merged branches
./branch_prune.py

# Delete them
./branch_prune.py --delete
```

## How it works
The script runs `git branch --merged` to get merged branches, filters out the current branch and protected ones (`master`, `main`, `develop`), then optionally deletes them using `git branch -d`.

## License
MIT © 2026
