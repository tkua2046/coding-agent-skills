# Freeze and push the first usable baseline

The user authorized fixing the current skills as the first version and pushing to
tkua2046/coding-agent-skills. VERSION already contains 0.1.0; retain it. Runtime
skill bytes are frozen to canonical-skills.json (39 files). This is the first usable
source baseline, with scoped validation and stated limits, not a claim that the
full release gate passed. No new skill changes or expensive model campaigns.

1. Publish the 12 complete existing evidence/package ZIPs (26.4MB total), checksums
   and an entry index on the existing separate evidence branch, retaining its
   parent history. No raw run snapshots enter the source tree. Verify remote
   archive/object identity and pin immutable links in docs/EVIDENCE.md.
2. Make a short first-baseline README/changelog/status update. Freeze completed
   notes under 0.1.0 dated 2026-09-29, keep Unreleased, and preserve earlier text.
   Keep existing formal release limits visible; no tag or hosted release is needed.
3. Review all intended maintained files, including the accumulated skill, tooling,
   fixture and documentation changes, excluding ignored artifacts. Run the full
   required fast checks and installed commit hook; preserve logs and any failures.
4. Commit and push codex/workflow-canary, update existing PR #1 around the actual
   first baseline, inspect remote CI and preserve final delivery evidence. A pending
   user preference asks whether to merge to main or retain the PR; do not infer a
   merge decision from elapsed time. Source push is already authorized.

The new source tree is approximately 832 files including four discovery symlinks;
39 are skill files. Most remaining files are versioned case fixtures, research,
tests and tooling, not execution outputs. The 2.8MB calibration.json contains known
scoring inputs/expectations used by tests, not an archive to silently drop at freeze.
Reviewability includes a simple usage entrypoint and evidence navigation.

Evidence publication uses Git archive objects without checking out source or
changing its index; normal source commits retain their installed hooks. Preserve
remote history and do not force-push. Evidence-only payloads receive ZIP CRC/hash,
manifest and credential-pattern checks, not source-code tests. Capture file scope
and exact published identities. Stop for a material finding, not a formatting preference.
