# Review the design

Read the original specifications, confirmed clarifications, relevant repository code, and the exact design version. Review without changing the design or product code. If asked for an independent review, use a separate agent context only when available and authorized; otherwise label this a self-review and disclose the limitation.

Look for missing or contradictory behavior, unexamined failure states, incompatible interfaces, unnecessary complexity, and decisions whose consequences are unclear. Use concrete scenarios, not stylistic preference alone, to justify required changes.

Also assess reading cost: can the first screen communicate the outcome and major choice? Are terms explained, examples decisive, sections navigable, and long detail separated from the main argument?

Output the review template: verdict, reviewed version/scope, checks actually performed, prioritized findings, and next action. Each finding needs a source location, trigger/example, consequence, minimal correction, and a way to verify the correction. Show the most important findings first; retain additional material issues in an appendix rather than hiding them.

Use `ready`, `needs changes`, or `needs decision`. A review is ready when material blockers are resolved and assumptions/nonblocking suggestions have dispositions, not when an arbitrary number of review passes has elapsed. A static review does not establish runtime correctness. Do not claim human approval or independent review that did not occur.
