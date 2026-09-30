Use the prepare-pr operation in skills/dev-workflow to prepare a local PR draft
for the actual setup/adaptation changes from the preceding task. This is a fresh
context: inspect the current working tree (including new files), original project
conventions and retained setup evidence. The setup changes themselves are the PR;
do not invent an application feature or perform another setup/design rewrite.

Write docs/reviews/PR.md with a concise, usable PR title and body. Make the concrete
user/contributor impact, actual current validation, relevant limits and next review
action easy to see. Reference detailed evidence rather than copying logs or a full
design. You may invoke the actual installed local hook and other existing offline
checks to verify the current changes; use CANARY_PYTHON when available. Do not
assume optional packages exist outside that prepared interpreter and do not install
anything. Preserve the prior task's evidence and distinguish past results from
checks you actually run now.

The maintainer's human review is pending and will happen after this handoff; do
not claim it occurred or stop drafting to request it. Preparing this local artifact
and executing local checks are already authorized. Apart from the draft and local
validation evidence, leave the setup changes intact. No remote PR creation,
commits, push, tags, version bump, release, external actions or additional review
rounds. Finish with the draft location and the remaining human review status.
