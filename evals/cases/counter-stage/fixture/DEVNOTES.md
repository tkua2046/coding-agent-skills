# Development gate
Run `python3 -m unittest discover -s tests -v` for focused checks and
`python3 hooks/pre-commit` for the full local gate before review and commit.
The runner installs this script as .git/hooks/pre-commit. Do not bypass it.
