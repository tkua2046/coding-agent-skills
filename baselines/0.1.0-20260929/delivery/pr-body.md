## First usable 0.1.0 source baseline

Provides four independently portable skills for feature design, implementation planning, stage development and delivery. Operations adapt their depth to uncertainty and consequences, keep plans focused on outcomes, preserve original requirements and verified review history, and finish with a readability check. Existing effective tools and checks are reused.

Start with the README or `docs/QUICKSTART.md`; install only the desired folders under `skills/`. The complete source tree has 832 paths, including 39 runtime skill files. Most remaining files are authored evaluation fixtures, safeguards and design/research records. Raw model executions and environment files are excluded from the source branch.

## Validation and evidence

- Independent aggregate review and final documentation review found no material blocker. All 39 skill files match the frozen manifest and tested portable package.
- Local mechanical tests: 390 passed; repository tooling coverage 94%. Initial hook formatting corrections are preserved, reviewed and restaged. Final normal commit hooks and both exact-head GitHub CI workflows passed.
- Scoped real model diagnostics include a same-conversation feature plus clarification and independent review in 221.447 seconds, with all independent functional checks passing. These do not mean all 60 evaluation cases passed.
- All 12 original evidence/package archives, including failed and inconclusive attempts, are downloadable with checksums from the [immutable evidence index](https://github.com/tkua2046/coding-agent-skills/blob/ecbb2533e6be9a9cec78acb9deb884ca66fce1db/baselines/0.1.0-20260929/README.md). Source documentation maps those archives to their original paths.

## Remaining limits

Full calibrated release qualification and interactive VS Code UI verification remain incomplete. A separate earlier workflow missed its 600-second target at 613.811 seconds; that failure is retained, and no causal speedup is claimed. This PR freezes a usable source baseline without creating a tag or GitHub Release. Current results and limitations are in `docs/VALIDATION.md`.
