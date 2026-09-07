# Session rejection stage

## Current handoff

Implementation is complete; stage acceptance is pending. Unknown commands raise
ValueError without changing cursor or selection, and subsequent valid movement
works. The contract also requires valid next/previous commands to update position
([original requirement](REQUEST.md)).

- Next action: run `python -m unittest discover -s tests -v`, the required gate in
  [DEVNOTES.md](DEVNOTES.md), when execution work resumes.
- Check status: that gate has not run on this resumed handoff. No checks were run
  during this documentation-only preparation; no passing gate is claimed.
- Open material findings: none. R1 is reviewer-verified fixed in the supplied
  [round 2 review](reviews/round2.md) for its matching candidate.
- Review policy: independent agent review plus human acceptance. Historical review
  is supplied evidence, not a new review performed by this handoff author.
- Human/owner acceptance: pending after the completed gate and required before
  any commit. The stage is not yet accepted; do not advance it.

## Candidate and evidence

The supplied source validates commands before either mutation. The supplied
regression asserts preservation of both fields on rejection and subsequent valid
`next` movement. The historical round 2 report identifies the reviewed content as:

| File | SHA-256 recorded in round 2 |
|---|---|
| [session.py](session.py) | `bfe24c031dc02cb821fc710ee9e7fbcf45fa562677728c35a40c8e9ef45d682a` |
| [tests/test_session.py](tests/test_session.py) | `38e1190859b65dc80a0b05642e76af6dba2345bff1eec88211b8b75a9bc2e0e6` |

These are the supplied review's content identities, not a claim that a new review
or test run occurred. Reuse that review only for matching content. No raw passing
test output is supplied; the historical inspection and pending execution gate are
separate evidence. This handoff changes only PLAN.md and creates no commit.

## Working policy

Preserve the [original requirement](REQUEST.md) and prior reviews. Current implementation and
review evidence are separate from human acceptance. New changes require affected
checks and a relevant recheck; a ready historical report is not evidence for a
changed candidate. Use [DEVNOTES.md](DEVNOTES.md) for the next required check.

A future commit requires that gate and owner acceptance. Review work is local;
there is no authorization to publish or change the version. A contributor should
inspect the intended change before committing and retain original failed checks.
This handoff preparation itself authorizes documentation only.

## Earlier progress

C1 implemented unknown-command rejection, but the original review found that both
cursor and selection changed before rejection. The original finding remains at
[round 1](reviews/round1.md). This is historical context, not the current disposition.

The later correction moved validation before mutation. Its independent review is
retained at [round 2](reviews/round2.md), including the content identity it checked.
Preserve these original reports when preparing a current handoff.

The exact incoming plan is preserved at
[plan before handoff](history/plan-before-handoff.md). The original reports remain
unchanged; round 1's open R1 is historical, superseded by round 2's verification
for the candidate recorded above.
