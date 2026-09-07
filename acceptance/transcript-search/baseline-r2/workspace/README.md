# Oral-history transcript viewer

An editor uses exported TSV cues to locate audio passages. Times are milliseconds;
text is displayed as supplied. The loader preserves file order and checks timing.

Show a transcript: `python transcript.py examples/interview.tsv`

Find a phrase: `python transcript.py examples/interview.tsv --find "phrase"`

Include up to two neighboring cues on each side of every match:
`python transcript.py examples/interview.tsv --find "phrase" --context 2`

Search is Unicode case-insensitive, but otherwise literal: punctuation and whitespace
in the phrase matter, and a phrase cannot continue from one cue into the next.
Overlapping context is printed once in transcript order. A search with no matches
prints nothing and succeeds. `--context` must be a nonnegative integer and may be
nonzero only when `--find` is used.

Run checks: `python -m unittest discover -s tests -v`

`Cue(start_ms, end_ms, text)`, `load_cues(path)`, `find_cues(cues, phrase, *,
context=0)` and `render_cues(cues)` are available to local scripts. `find_cues`
returns a new list and does not modify the supplied cues.
