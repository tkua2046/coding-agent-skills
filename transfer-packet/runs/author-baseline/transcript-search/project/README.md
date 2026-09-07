# Oral-history transcript viewer

An editor uses exported TSV cues to locate audio passages. Times are milliseconds;
text is displayed as supplied. The loader preserves file order and checks timing.

Show a transcript: `python transcript.py examples/interview.tsv`

Run checks: `python -m unittest discover -s tests -v`

`Cue(start_ms, end_ms, text)`, `load_cues(path)` and `render_cues(cues)` are used by
another local script. Keep these interfaces and the existing output compatible.
