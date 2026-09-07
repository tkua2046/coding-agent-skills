"""Preview or import a local workshop handout ZIP packet."""

import argparse
import os
import shutil
import stat
import tempfile
import zlib
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def _validated_members(packet):
    """Return members after validating their names, relationships, and types."""
    members = packet.infolist()
    paths = {}

    for member in members:
        name = member.filename
        is_directory = member.is_dir()

        if not name or name.startswith("/") or "\\" in name or ":" in name:
            raise ValueError(f"invalid ZIP member path: {name!r}")

        path_name = name[:-1] if is_directory else name
        components = path_name.split("/")
        if not path_name or any(part in ("", ".", "..") for part in components):
            raise ValueError(f"invalid ZIP member path: {name!r}")

        path = tuple(components)
        if path in paths:
            raise ValueError(f"duplicate or conflicting ZIP member path: {path_name!r}")
        paths[path] = is_directory

        if member.create_system == 3:
            file_type = stat.S_IFMT(member.external_attr >> 16)
            expected_type = stat.S_IFDIR if is_directory else stat.S_IFREG
            if file_type not in (0, expected_type):
                raise ValueError(f"unsupported ZIP member type: {name!r}")

    for path in paths:
        for length in range(1, len(path)):
            parent = path[:length]
            if parent in paths and not paths[parent]:
                raise ValueError(
                    f"ZIP file is used as a parent directory: {'/'.join(parent)!r}"
                )

    return members


def preview(archive):
    """Validate an archive and return its sorted relative file names."""
    with ZipFile(archive) as packet:
        members = _validated_members(packet)
        return sorted(member.filename for member in members if not member.is_dir())


def import_packet(archive, destination):
    """Validate and atomically import an archive into a new destination."""
    destination = Path(destination)
    if os.path.lexists(destination):
        raise FileExistsError(f"destination already exists: {destination}")

    temporary = None
    try:
        try:
            with ZipFile(archive) as packet:
                members = _validated_members(packet)
                names = sorted(member.filename for member in members if not member.is_dir())
                temporary = Path(
                    tempfile.mkdtemp(prefix=f".{destination.name}.tmp-", dir=destination.parent)
                )
                for member in members:
                    target = temporary.joinpath(*member.filename.rstrip("/").split("/"))
                    if member.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with packet.open(member) as source, target.open("xb") as output:
                            shutil.copyfileobj(source, output)
        except zlib.error as error:
            raise BadZipFile(f"corrupt compressed data: {error}") from error

        # Closing the archive before placement keeps every archive/read failure on
        # the temporary side of the all-at-once visibility boundary.
        os.rename(temporary, destination)
    finally:
        if temporary is not None and temporary.exists():
            shutil.rmtree(temporary)

    return names


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
