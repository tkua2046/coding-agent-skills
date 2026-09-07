# Session rejection stage

The current stage state is recorded under Current delivery below.

## Working policy

Preserve the original requirement and prior reviews. Current implementation and
review evidence are separate from human acceptance. New changes require affected
checks and a relevant recheck; a ready historical report is not evidence for a
changed candidate. Use the contributor guide for the next required check.

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

## Current delivery

Implementation is complete: unknown commands preserve cursor and selection while
raising ValueError, and a later valid movement still works. R1 is reviewer verified
fixed on the supplied unchanged source and test content. No material finding is
open. The required resumed gate has not run; human acceptance is also pending.
Next: run the DEVNOTES gate, then obtain owner acceptance before any commit.
