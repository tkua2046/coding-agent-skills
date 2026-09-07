"""Read an editor's TSV export and print a timestamped transcript."""
import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Cue:
    start_ms: int
    end_ms: int
    text: str


def load_cues(path):
    cues = []
    with Path(path).open(encoding="utf-8", newline="") as stream:
        rows = csv.DictReader(stream, delimiter="\t")
        if rows.fieldnames != ["start_ms", "end_ms", "text"]:
            raise ValueError("expected start_ms, end_ms, text columns")
        for number, row in enumerate(rows, 2):
            try:
                start, end = int(row["start_ms"]), int(row["end_ms"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"line {number}: invalid timestamp") from error
            if start < 0 or end <= start:
                raise ValueError(f"line {number}: invalid time interval")
            if cues and start < cues[-1].start_ms:
                raise ValueError(f"line {number}: cues must be in time order")
            if row["text"] is None or None in row:
                raise ValueError(f"line {number}: invalid text column")
            cues.append(Cue(start, end, row["text"]))
    return cues


def timestamp(milliseconds):
    seconds, millis = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"


def render_cues(cues):
    return "\n".join(
        f"{timestamp(cue.start_ms)} --> {timestamp(cue.end_ms)} {cue.text}"
        for cue in cues
    )


def find_cues(cues, phrase, *, context=0):
    """Return cues matching phrase, with neighboring cues for context."""
    if not isinstance(phrase, str) or not phrase.strip():
        raise ValueError("phrase must contain non-whitespace text")
    if isinstance(context, bool) or not isinstance(context, int) or context < 0:
        raise ValueError("context must be a nonnegative integer")

    cue_list = list(cues)
    selected = set()
    folded_phrase = phrase.casefold()
    for index, cue in enumerate(cue_list):
        if folded_phrase in cue.text.casefold():
            start = max(0, index - context)
            stop = min(len(cue_list), index + context + 1)
            selected.update(range(start, stop))
    return [cue for index, cue in enumerate(cue_list) if index in selected]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--find", metavar="PHRASE", help="show cues containing PHRASE")
    parser.add_argument(
        "--context",
        type=int,
        default=0,
        metavar="N",
        help="include up to N neighboring cues on each side of a match",
    )
    args = parser.parse_args()
    try:
        if args.context < 0:
            raise ValueError("context must be a nonnegative integer")
        if args.find is None and args.context:
            raise ValueError("--context requires --find")

        cues = load_cues(args.file)
        if args.find is not None:
            cues = find_cues(cues, args.find, context=args.context)
        output = render_cues(cues)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if output:
        print(output)


if __name__ == "__main__":
    main()
