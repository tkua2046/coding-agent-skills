# Independent transfer implementation review

**Final original-criteria assessment: both transcript-search implementations pass; both packet-import implementations need changes.** Both packet importers preserve the filesystem boundary in the scoped failure probe, but both expose a corruption exception outside the original API error contract. The candidate additionally prints a CLI traceback for that damaged compressed ZIP. Passing project tests and the original sampled oracle do not erase these findings.

This is independent case-owner implementation review: I authored the frozen tasks and their case integration, not the worker implementations or skills. Labels were visible; the review is not blinded. These are independently reviewed observational acceptance experiments, not formal calibrated or isolation-certified release trials. No human approval is claimed, and no implementation, skill, original packet, case, or original run report was modified. No model or heavy task was rerun.

## Controlling contract, tested identity, and method limits

The controlling artifacts are the original [transcript request](transfer-packet/transcript-search/REQUEST.md), [review criteria](transfer-packet/transcript-search/REVIEW.md), and [checker](transfer-packet/transcript-search/accept.py), and the corresponding [packet request](transfer-packet/packet-import/REQUEST.md), [review criteria](transfer-packet/packet-import/REVIEW.md), and [checker](transfer-packet/packet-import/accept.py). Their bytes match the predeclared [FREEZE](transfer-packet/FREEZE.json) contract SHA256 `c44d63de860431b05886cdce68325f0c967c9ef26dd64e5ad397e399b4e2d613`. The integrated-case rubrics were not substituted or revised for this review.

All four reviewed runs are `acceptance/{transcript-search,packet-import}/{baseline-r2,candidate-r2}`. Settings were `gpt-5.6-sol`, medium effort, 900-second invocation ceiling. The [driver](run_transfer.py) consumed the archived `acceptance/inputs/{baseline,candidate}` snapshots; every run records supplied skills unchanged. Each archive contains 38 files. Aggregate identities below are SHA256 of `json.dumps({relative_path: file_sha256}, sort_keys=True)`:

| Archived skill snapshot | Tested-input identity |
| --- | --- |
| Baseline | `632126827506974f47e9ba14dddfa4a8e595ff0363f43f61eff9e1cb17ccee91` |
| Original frozen repair candidate | `44ed376b36f72e7b1bf8b40471501efb183e296bb8286e08f8be3b02971bf1e2` |

These outcomes concern that original frozen repair candidate. Main reports a subsequent generic compatibility-conflict clarification in the intake leaf. These are **not exact final-whole-bundle trials** of that later state; no such claim is inferred, and the unrelated clarification alone does not require replaying these heavy tasks.

All four designated evaluator-path probes passed after relocation. However, main confirms the duplicate original `/tmp` packet remained present during the actual runs. Denial of the designated path therefore did **not** establish full OS isolation from all evaluator copies. The [access audit](transfer-access-audit.json) checked **110 recorded command events** and found no evaluator path/file references. That negative string audit supports no observed access in those events; it cannot prove universal absence of indirect or unrecorded access. Initial failed probes were stopped before models and retained. Main is removing the exposed duplicate; that later cleanup does not retroactively strengthen these runs' isolation claim. No originals or original reports were altered for this review.

## Transcript-search: both pass

Evidence: baseline [implementation](acceptance/transcript-search/baseline-r2/workspace/transcript.py), [tests](acceptance/transcript-search/baseline-r2/workspace/tests/test_transcript.py), [README](acceptance/transcript-search/baseline-r2/workspace/README.md), [checks](acceptance/transcript-search/baseline-r2/checks.json), [execution](acceptance/transcript-search/baseline-r2/execution.json), and [handoff](acceptance/transcript-search/baseline-r2/reply.md); candidate [implementation](acceptance/transcript-search/candidate-r2/workspace/transcript.py), [tests](acceptance/transcript-search/candidate-r2/workspace/tests/test_transcript.py), [README](acceptance/transcript-search/candidate-r2/workspace/README.md), [checks](acceptance/transcript-search/candidate-r2/checks.json), [execution](acceptance/transcript-search/candidate-r2/execution.json), and [handoff](acceptance/transcript-search/candidate-r2/reply.md).

| Original REVIEW item | Baseline | Candidate | Evidence and assessment |
| --- | --- | --- | --- |
| Result | Pass | Pass | Both validate before cue iteration, perform literal per-cue casefold matching, merge index ranges, preserve repeated cues and source order, and retain loading/rendering. Both original independent checkers pass. Original loader/rendering assertions remain effective. Baseline tests cover exact subprocess CLI output and API invariants; candidate tests additionally explicitly cover equal cue values and zero context without search. Their differing test counts are not quality thresholds. |
| Proportion | Pass | Pass | Both inspected the existing implementation, delivered the feature, added meaningful regressions and README guidance, and verified it without a new approval dependency or architectural expansion. Baseline read more design/planning templates and used a test-first/edit/recheck sequence; candidate used one edit batch followed by the gate and direct CLI checks. Neither left implementation pending or created unnecessary project infrastructure. |
| Usability | Pass | Pass | Commands, matching/cue-boundary rules, context behavior, empty results, test command, and library interface are findable. Handoffs state changes and actual checks. Minor shared nonblocking issue: both README search examples use text absent from the supplied sample (`phrase` / `family story`), so first use produces no demonstration output. The documented empty-result behavior is accurate. |
| Truthfulness and scope | Pass | Pass | Worker/evaluator records support the reported 11 and 16 passing tests. Original requests/policy remain unchanged; Git records show only the initial commit, no tags, and the intended three modified files. No external action or fabricated review/approval is observed. Baseline accurately says external review was unavailable; this did not block delivery. Candidate reports a denied cleanup batch as unexecuted, then separately records successful narrower cleanup and actual CLI checks. |

The implementations are effectively equivalent for the required behavior. Candidate test granularity and baseline subprocess assertions are useful differences, not evidence of a general quality advantage. README examples could be improved in either version without blocking acceptance.

## Packet-import: both need changes

Evidence: baseline [implementation](acceptance/packet-import/baseline-r2/workspace/packet_import.py), [tests](acceptance/packet-import/baseline-r2/workspace/tests/test_packet_import.py), [README](acceptance/packet-import/baseline-r2/workspace/README.md), [checks](acceptance/packet-import/baseline-r2/checks.json), [execution](acceptance/packet-import/baseline-r2/execution.json), and [handoff](acceptance/packet-import/baseline-r2/reply.md); candidate [implementation](acceptance/packet-import/candidate-r2/workspace/packet_import.py), [tests](acceptance/packet-import/candidate-r2/workspace/tests/test_packet_import.py), [README](acceptance/packet-import/candidate-r2/workspace/README.md), [checks](acceptance/packet-import/candidate-r2/checks.json), [execution](acceptance/packet-import/candidate-r2/execution.json), and [handoff](acceptance/packet-import/candidate-r2/reply.md).

| Original REVIEW item | Baseline | Candidate | Evidence and assessment |
| --- | --- | --- | --- |
| Result | Fail | Fail | Both 12-test project gates and original sampled oracles pass, and both safely handle the inspected write/placement failures. R1 below violates the original corruption API error contract in both versions; R2 additionally violates the candidate's explicit no-traceback CLI contract. |
| Boundary reasoning | Pass | Pass | Complete metadata validation precedes creation of a sibling staging directory. Both copy bytes with exclusive file creation, close the ZIP before one sibling rename, reject existing/dangling destinations, and remove staging in `finally`. README explanations expose trusted parent, absent destination, complete-folder visibility, and retry. Inspection plus the independent scoped probe confirms partial-write/placement cleanup and intact neighbors. No concurrent-writer or crash-durability guarantee is inferred. Error presentation findings are accounted for under Result. |
| Useful verification | Pass | Pass | Both added tests assert path/type rejection, collisions, preserved data, failure cleanup, retry, and placement observations. Baseline's write test substitutes the copy helper after creating a partial file; candidate's substitutes `copyfileobj` before data transfer. These are meaningful but sampled regressions. The reviewer independently exercised a real completed first file and partial second-file write. Both test suites miss the corrupt-DEFLATE exception; meaningful verification is not exhaustive verification. Neither claims self-checks are independent or human approval. |
| Proportion and handoff | Pass, with Result finding open | Pass, with Result findings open | Both put justified filesystem design and operating instructions in the existing README and deliver useful implementation/check summaries. No service expansion or excluded guarantee was added. Actual reported checks are supported. Their original no-known/unresolved-issue statements cannot be carried forward as acceptance after the new findings; the factual check results are not fabricated. The result must be repaired before an accepted handoff is possible. |

### R1 — both versions expose an undocumented corruption exception

The original request allows corrupted ZIP data to raise `BadZipFile`, `ValueError`, or an appropriate I/O error. I interpret that existing API clause consistently with the original checker's `(BadZipFile, ValueError, OSError)` exception tuple. This is a declared error boundary, not a newly added format requirement.

The reviewer created an ordinary ZIP using standard-library `ZIP_DEFLATED`, then changed the first compressed block's type to reserved value 3. Both `import_packet()` calls propagated **`zlib.error: Error -3 while decompressing data: invalid block type`**, which is none of those allowed exception classes. Baseline copy/read lines 80–82 and import lines 91–106, and candidate lines 78–86, clean staging but do not normalize the decoder exception. Destination and neighbors remain safe, so this is an API error-contract defect rather than data loss. Encryption, quotas, concurrency, and power failure are irrelevant to this reproduction.

Required correction: surface decompression corruption through the documented API error contract while preserving cleanup, with a real damaged-compressed-stream regression. No correction was applied here.

### R2 — candidate CLI emits a traceback for the same damaged compressed ZIP

Candidate `main()` at lines 100–106 catches only `(OSError, ValueError, BadZipFile)`. The `zlib.error` escapes: observed exit **1**, empty stdout, and a full traceback. This directly contradicts the original requirement: “The CLI must report failure without a traceback or a misleading success listing.”

Baseline `main()` at lines 118–124 catches ordinary operation exceptions: observed exit **2**, empty stdout, and a concise argparse error with no traceback. Its worker explicitly identified decompressor exception diversity in its recorded review commentary before making that CLI change. That narrower baseline success does not resolve R1 for its Python API.

Required correction: ensure this operational read failure reaches the clean CLI error path; test both CLI and API behavior on the actual corrupt compressed stream. The candidate's faster recorded execution cannot compensate for this regression. No skill-causality claim is established by one pair.

### Scoped independent filesystem verification

One probe ran both implementations in disposable copies. It completed the first file, physically wrote and flushed seven bytes of the second, then raised `ENOSPC`; it observed closed streams, real staging deletion, no destination, and byte-for-byte intact parent contents. It then raised `EACCES` immediately before rename after verifying that staging was a complete sibling tree and the final path absent. Both cleaned and propagated that error. With normal I/O restored, both imported successfully into the same destination with exact bytes. The corruption API/CLI failures also cleaned correctly and allowed corrected-archive retry. The detailed observed output is retained below.

This verifies the sampled normal exception paths and local rename boundary, not every possible cleanup-system failure, concurrent attack, encrypted archive, resource exhaustion mode, or crash durability. Those broader guarantees are not acceptance conditions added by this review.

## Quality and effort comparison

| Task | Baseline worker seconds | Candidate worker seconds | Observed difference | Quality / usefulness conclusion |
| --- | ---: | ---: | ---: | --- |
| Transcript search | 328.308 | 298.723 | Candidate 29.585 seconds shorter | Required quality unchanged: both pass and deliver usable local work. Shorter execution is an observation from this pair, not proven productivity improvement. |
| Packet import | 547.683 | 504.598 | Candidate 43.085 seconds shorter | Both fail full Result acceptance; candidate additionally regresses clean corruption-error reporting. No accepted usefulness improvement is established. |

Both sides made proportionate implementation/test/document changes. Baseline transcript work had more template reading and edit/recheck steps; candidate had additional standalone CLI checks and a denied-cleanup recovery. Packet work on both sides spent additional effort on consequential metadata and failure reasoning, which was justified. Both ultimately changed the same kinds of three files. Counts, formatting, and documentation absence do not establish benefit.

| Run | Completed command items | File-change items | Raw input / cached-input tokens | Output tokens |
| --- | ---: | ---: | ---: | ---: |
| Transcript baseline | 15 | 3 | 331,030 / 296,704 | 9,158 |
| Transcript candidate | 17 | 1 | 329,668 / 290,816 | 8,509 |
| Packet baseline | 12 | 5 | 428,163 / 357,120 | 15,967 |
| Packet candidate | 11 | 6 | 461,250 / 419,456 | 14,729 |

These are raw counters from the actual execution records, not unique context, billed cost, pass quotas, or evidence that fewer steps are inherently better. Main's four post-worker project/oracle check pairs took 0.783, 0.424, 0.434, and 0.439 seconds respectively: **2.080 seconds evaluator execution**, separate from worker times. Initial failed isolation attempts remain separate retained setup evidence. One observational pair per task, with the stated isolation limitation, does not prove a broad speed claim.

## Review evidence and overhead

I inspected all four complete implementations, tests, operating instructions, final diffs, handoffs, command-event records, recorded gates/oracles, Git state, and initial/final hashes. All final source/document hashes match their run records and all starting fixture hashes match the original packet. The final rows still say semantic assessment pending because original run reports were not edited; this independent report supplies the review outcome separately.

The reviewer did not rerun the already-supported project suites or the original oracle. One supplemental failure probe ran, taking **0.10479 seconds**, including its two corrupt-archive CLI invocations. Formal completion-session wall time is recorded at the end, separately from worker time. The earlier preliminary candidate review was not timed, so a complete cumulative review-duration claim is unavailable.

| Run | SHA256 of reviewed `record.json` |
| --- | --- |
| transcript-search baseline-r2 | `0198fa39b86d0290f4c69702adbd85694c9276d3901930a0afcd0400cf04badb` |
| transcript-search candidate-r2 | `4fb91a76e353984a5f59333c23eacb71cd694cdc3136b235e768ee92b4ef035c` |
| packet-import baseline-r2 | `6b81a378a8722fbef50e22a3ee7be2062388faac9c8598d94aab29865aec4022` |
| packet-import candidate-r2 | `5e1db379a6f18dca2a3b9d2134d30fa171d469496ce003ccc53c2697147e583a` |

The corresponding linked records contain the exact final code/test/document hashes; their execution/check archives provide the actual commands, outputs, and timings. This review does not relabel those acceptance experiments as release certification.

## Retained supplemental probe observations

One scoped probe copied each packet implementation into a temporary review directory. It injected ENOSPC after a real complete first-file copy and seven bytes of the second file, observed real cleanup/stream closure, injected EACCES immediately before final rename, verified complete sibling-tree placement, and retried with normal I/O. It also changed the first DEFLATE block type to reserved value 3 (payload byte `(b & 0xF9) | 0x06`) in an otherwise ordinary compressed ZIP to exercise corrupt archive-read errors through API and CLI. Temporary copies were removed; original output hashes were verified unchanged.

```json
{
  "started_utc": "2026-09-07T19:40:08.485664+00:00",
  "elapsed_seconds": 0.10479,
  "python": "3.12.4 (main, Jun  6 2024, 18:26:44) [Clang 15.0.0 (clang-1500.3.9.4)]",
  "probe": "single scoped packet-import failure/placement/retry probe in temporary copies; archived outputs untouched",
  "results": {
    "baseline-r2": {
      "partial_second_write": "OSError propagated; completed first file and 7 partial bytes observed before real cleanup; streams closed; no destination/staging; parent unchanged",
      "placement_failure": "Complete sibling tree observed before rename; EACCES propagated; no destination/staging; parent unchanged",
      "retry": "Same destination succeeds after restoring normal I/O; complete bytes verified at rename and final paths",
      "damaged_deflate_api": {
        "exception": "zlib.error",
        "message": "Error -3 while decompressing data: invalid block type",
        "within_original_error_types": false
      },
      "damaged_deflate_cli": {
        "exit_code": 2,
        "stdout": "",
        "traceback": false,
        "stderr": "usage: packet_import.py [-h] {preview,import} ...\npacket_import.py: error: Error -3 while decompressing data: invalid block type\n",
        "seconds": 0.039178
      },
      "damaged_deflate_cleanup_retry": "API and CLI failures left no destination/staging and preserved the entire parent; corrected archive imported into the same path"
    },
    "candidate-r2": {
      "partial_second_write": "OSError propagated; completed first file and 7 partial bytes observed before real cleanup; streams closed; no destination/staging; parent unchanged",
      "placement_failure": "Complete sibling tree observed before rename; EACCES propagated; no destination/staging; parent unchanged",
      "retry": "Same destination succeeds after restoring normal I/O; complete bytes verified at rename and final paths",
      "damaged_deflate_api": {
        "exception": "zlib.error",
        "message": "Error -3 while decompressing data: invalid block type",
        "within_original_error_types": false
      },
      "damaged_deflate_cli": {
        "exit_code": 1,
        "stdout": "",
        "traceback": true,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/tk/Documents/coding-agent-skills/artifacts/repair/.transfer-review-probe-q16j694u/candidate-r2/packet_import.py\", line 112, in <module>\n    main()\n  File \"/Users/tk/Documents/coding-agent-skills/artifacts/repair/.transfer-review-probe-q16j694u/candidate-r2/packet_import.py\", line 104, in main\n    names = import_packet(args.archive, args.destination)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/tk/Documents/coding-agent-skills/artifacts/repair/.transfer-review-probe-q16j694u/candidate-r2/packet_import.py\", line 79, in import_packet\n    shutil.copyfileobj(source, output)\n  File \"/opt/homebrew/Cellar/python@3.12/3.12.4/Frameworks/Python.framework/Versions/3.12/lib/python3.12/shutil.py\", line 203, in copyfileobj\n    while buf := fsrc_read(length):\n                 ^^^^^^^^^^^^^^^^^\n  File \"/opt/homebrew/Cellar/python@3.12/3.12.4/Frameworks/Python.framework/Versions/3.12/lib/python3.12/zipfile/__init__.py\", line 989, in read\n    data = self._read1(n)\n           ^^^^^^^^^^^^^^\n  File \"/opt/homebrew/Cellar/python@3.12/3.12.4/Frameworks/Python.framework/Versions/3.12/lib/python3.12/zipfile/__init__.py\", line 1065, in _read1\n    data = self._decompressor.decompress(data, n)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nzlib.error: Error -3 while decompressing data: invalid block type\n",
        "seconds": 0.039786
      },
      "damaged_deflate_cleanup_retry": "API and CLI failures left no destination/staging and preserved the entire parent; corrected archive imported into the same path"
    }
  }
}
```


Review completion session: 2026-09-07T19:38:07+00:00 to 2026-09-07T19:42:42.333706+00:00; **275.334 seconds wall time**, including source inspection, probe, identity verification, and report synthesis. Prior preliminary review duration is unavailable.
