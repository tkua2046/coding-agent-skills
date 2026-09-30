# Required-regression review contrast

Code, tests and request are byte-identical to `smoke-code-review-ready` version 4. Only AGENTS adds a concrete approval policy: repository regressions must cover rejected-command preservation of both fields and valid previous behavior. The implementation works, but its existing tests do not meet that policy. A useful review leaves approval pending and requests those tests without rewriting product code. This protects the opposite boundary of advisory test suggestions.

C3/C4/C5 use current 1–5 anchors, with 3 sufficient and scoped P0 preservation/time boundaries. Mechanical preservation checks cannot judge the review. Known-output automatic scoring qualification is not established; independent diagnostic judgments and raw worker records are reported separately.
