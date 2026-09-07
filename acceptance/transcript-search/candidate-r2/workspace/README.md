# Oral-history transcript viewer

An editor uses exported TSV cues to locate audio passages. Times are milliseconds;
text is displayed as supplied. The loader preserves file order and checks timing.

Show a transcript: `python transcript.py examples/interview.tsv`

Find cues containing a phrase: `python transcript.py examples/interview.tsv --find "family story"`

Include up to two neighboring cues before and after every match:
`python transcript.py examples/interview.tsv --find "family story" --context 2`

Search is Unicode case-insensitive and treats punctuation and whitespace literally, so
quote phrases containing spaces or shell punctuation. A phrase must contain at least
one non-whitespace character. Matches stay within individual cues; phrases cannot span
two cues. Overlapping context is printed only once in transcript order, and a search
with no matches prints nothing and succeeds. `--context` is a nonnegative integer and
a value greater than zero requires `--find`.

Run checks: `python -m unittest discover -s tests -v`

`Cue(start_ms, end_ms, text)`, `load_cues(path)`, `find_cues(cues, phrase, *,
context=0)` and `render_cues(cues)` are available to other local scripts. The search
function returns a new list and does not modify the supplied cues.
