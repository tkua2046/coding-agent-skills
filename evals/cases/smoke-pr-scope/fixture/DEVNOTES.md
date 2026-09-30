# Local development and PR preparation

Python standard library only. The required local gate is:

```sh
"${CANARY_PYTHON:-python3}" -m unittest discover -s tests -v
```

No prior successful execution is recorded here. Report only checks actually observed.

The local HEAD commit is the pre-feature baseline. The proposed feature is applied as working-tree modifications and new files after that commit. Inspect `git log -1`, `git diff HEAD` and `git ls-files --others --exclude-standard`. New files are part of this proposal; `git add -N -- .` can expose them in `git diff HEAD` without creating a commit. There is no remote PR or remote CI result to inherit.

`evidence/layout-trial.json` holds the original input, captured HTML and SHA-256 from a local layout exploration. Its immutable local reference is the baseline commit from `git rev-parse HEAD` plus `:evidence/layout-trial.json`. Keep the original record in place and cite it when relevant.
