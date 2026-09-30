# Optional review shape

Review owns a revision-bound verdict and actionable findings, not a rewritten plan or duplicated delivery status. A sufficient review may be a short response.

Verdict: [ready / needs changes / needs decision, with material open concerns].
Scope and evidence: [reviewed revision, actual independent/self-review, checks and limits].

[For each material finding: location, trigger, consequence, smallest correction and verification. Stable IDs help when findings need rechecking.]

Example: R1, stage order — the import stage promises writes before validation is available. An invalid row could then change stored data. Make validation a prerequisite of the first mutating stage; verify invalid input causes no writes. Open pending correction and recheck.

On recheck, link the original finding and reviewed revision; record what changed and the supported disposition. Preserve originals through existing immutable references, capturing unavailable content once. Author-reported fixes, reviewer-verified closure and human acceptance are different states. Partial fixes stay open; complete verified fixes close. Nonblocking preferences need no correction round.
