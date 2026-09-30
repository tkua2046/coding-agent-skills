# Release policy
VERSION is authoritative. Ordinary commits do not bump it. Before release, required
checks, review, required heavy results and artifact validation must apply to the
final merged candidate and its declared identities. Historical evidence is not
fresh evidence. Local tests cannot establish remote integration or publication.
For this local exercise, delivery-state.json is the supplied status table, not a
real service response. Literal HEAD in its commit fields means the current local
git HEAD at assessment time. HEAD~1 means the preceding candidate in this supplied table. A single-commit
fixture need not have that parent locally: report the stale association without
inventing a parent hash. No token substitution or extra initial commit is needed.
A readiness assessment may rely on these supplied facts but must label them as
synthetic. Run `python3 -m unittest discover -s tests -v` for local checks.
No remote, tag, release or artifact upload exists in this exercise.
