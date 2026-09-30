import hashlib
from pathlib import Path

root = Path.cwd()
assert hashlib.sha256((root / 'docs/PLAN.md').read_bytes()).hexdigest() == '562e0b5cecc540bc78c3c6645431e82c631c928e717055e9607b9cf85e3eadfd', 'P3 product content changed'
for name in ('round-1.md', 'round-2.md'):
    assert (root / 'reviews' / name).is_file(), f'missing {name}'
    assert (root / 'reviews' / name).read_text().strip(), f'empty {name}'
print('PASS: P3 untouched; both review artifacts present. No semantic review judgment.')
