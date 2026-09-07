"""Preview or import a local workshop handout ZIP packet."""
import argparse
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def preview(archive):
    with ZipFile(archive) as packet:
        return sorted(member.filename for member in packet.infolist() if not member.is_dir())


def import_packet(archive, destination):
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    with ZipFile(archive) as packet:
        destination.mkdir()
        packet.extractall(destination)
        return sorted(member.filename for member in packet.infolist() if not member.is_dir())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("preview")
    listing.add_argument("archive", type=Path)
    importing = commands.add_parser("import")
    importing.add_argument("archive", type=Path)
    importing.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "preview":
            names = preview(args.archive)
        else:
            names = import_packet(args.archive, args.destination)
    except (OSError, ValueError, BadZipFile) as error:
        parser.error(str(error))
    for name in names:
        print(name)


if __name__ == "__main__":
    main()
