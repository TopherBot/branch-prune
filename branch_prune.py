#!/usr/bin/env python3
"""branch-prune: tiny tool to list or delete merged local git branches.

Usage:
  ./branch_prune.py          # show merged branches (dry‑run)
  ./branch_prune.py --delete # delete them after confirmation
"""
import subprocess, sys, argparse

def run_git(args):
    result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_merged_branches():
    out = run_git(['branch', '--merged'])
    branches = [line.strip().lstrip('* ').strip() for line in out.splitlines()]
    # Exclude current branch and common protected branches
    protected = {'master', 'main', 'develop'}
    current = run_git(['rev-parse', '--abbrev-ref', 'HEAD'])
    filtered = [b for b in branches if b and b != current and b not in protected]
    return filtered

def delete_branch(branch):
    try:
        run_git(['branch', '-d', branch])
        print(f'Deleted {branch}')
    except subprocess.CalledProcessError as e:
        print(f'Failed to delete {branch}: {e.stderr.strip()}', file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='List or delete merged local git branches')
    parser.add_argument('--delete', action='store_true', help='Delete the listed branches')
    args = parser.parse_args()
    try:
        merged = get_merged_branches()
    except subprocess.CalledProcessError:
        print('Not a git repository or git command failed.', file=sys.stderr)
        sys.exit(1)
    if not merged:
        print('No merged branches to clean.')
        return
    print('Merged branches:')
    for b in merged:
        print('  ', b)
    if args.delete:
        confirm = input('Delete these branches? [y/N] ').lower()
        if confirm == 'y':
            for b in merged:
                delete_branch(b)
        else:
            print('Aborted.')

if __name__ == '__main__':
    main()
