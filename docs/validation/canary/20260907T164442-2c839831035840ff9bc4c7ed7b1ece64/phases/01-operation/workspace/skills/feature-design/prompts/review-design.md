# Review the design

Read the original specifications, confirmed clarifications, relevant repository code, and the exact design version. Review without changing the design or product code. If asked for an independent review, use a separate agent context only when available and authorized; otherwise label this a self-review and disclose the limitation.

Assess the requested decisions at the chosen task depth. A combined design/plan note is acceptable when its contract and next outcome are clear; do not demand separate artifacts merely to match a template. Review already sufficient work to a ready verdict.

Look for missing or contradictory behavior, unexamined failure states, incompatible interfaces, unnecessary complexity, and decisions whose consequences are unclear. Use concrete scenarios, not stylistic preference alone, to justify required changes.

Also assess reading cost: can the first screen communicate the outcome and major choice? Are terms explained, examples decisive, sections navigable, and long detail separated from the main argument?

Output the review template: verdict, reviewed version/scope, checks actually performed, prioritized findings, and next action. Each finding needs a source location, trigger/example, consequence, minimal correction, and a way to verify the correction. Show the most important findings first; retain additional material issues in an appendix rather than hiding them.

Use `ready`, `needs changes`, or `needs decision`. A review is ready when material blockers are resolved and assumptions/nonblocking suggestions have dispositions, not when an arbitrary number of review passes has elapsed. A static review does not establish runtime correctness. Do not claim human approval or independent review that did not occur.

On recheck, put the current verdict, candidate version, open finding IDs and next action first. Keep stable finding IDs and the original round. Distinguish the author's “fixed” claim from the reviewer's verified resolution; cite the changed content and recheck the full affected invariant. For example, preserving heading still fails a requirement to preserve both position and heading. Append round/disposition evidence rather than overwriting the original concern. Review unaffected decisions again only if new evidence puts them in doubt. A repeated disagreement with no new evidence calls for a bounded check or a clearly stated decision, not another cosmetic rewrite. Reaching a time budget does not resolve a blocker; preserve the open issue and the evidence needed to proceed.
