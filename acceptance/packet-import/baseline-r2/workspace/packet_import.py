"""Preview or import a local workshop handout ZIP packet."""

import argparse
import os
import shutil
import stat
import tempfile
from pathlib import Path
from zipfile import ZipFile


def _validated_members(packet):
    """Return validated (ZipInfo, relative parts, is_directory) records."""
    members = []
    paths = {}

    for member in packet.infolist():
        name = member.filename
        is_directory = member.is_dir()

        if not name:
            raise ValueError("archive member has an empty path")
        if name.startswith("/"):
            raise ValueError(f"archive member has an absolute path: {name!r}")
        if "\\" in name:
            raise ValueError(f"archive member contains a backslash: {name!r}")
        if ":" in name:
            raise ValueError(f"archive member contains a colon: {name!r}")

        path_text = name[:-1] if is_directory else name
        parts = tuple(path_text.split("/"))
        if any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"archive member has an invalid path component: {name!r}")

        if member.create_system == 3:
            file_type = stat.S_IFMT(member.external_attr >> 16)
            if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError(f"archive member has a special Unix file type: {name!r}")
            if file_type == stat.S_IFDIR and not is_directory:
                raise ValueError(f"archive directory metadata conflicts with its path: {name!r}")
            if file_type == stat.S_IFREG and is_directory:
                raise ValueError(f"archive file metadata conflicts with its path: {name!r}")

        if parts in paths:
            raise ValueError(f"archive contains a duplicate or conflicting path: {name!r}")
        for length in range(1, len(parts)):
            parent = parts[:length]
            if paths.get(parent) is False:
                raise ValueError(
                    f"archive file is used as a parent directory: {'/'.join(parent)!r}"
                )
        if not is_directory and any(
            len(other) > len(parts) and other[: len(parts)] == parts for other in paths
        ):
            raise ValueError(f"archive file is used as a parent directory: {name!r}")

        paths[parts] = is_directory
        members.append((member, parts, is_directory))

    return members


def _file_names(members):
    return sorted(member.filename for member, _, is_directory in members if not is_directory)


def preview(archive):
    """Validate an archive and return its sorted relative file names."""
    with ZipFile(archive) as packet:
        return _file_names(_validated_members(packet))


def _copy_members(packet, members, staging):
    for member, parts, is_directory in members:
        target = staging.joinpath(*parts)
        if is_directory:
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        with packet.open(member, "r") as source, target.open("xb") as output:
            shutil.copyfileobj(source, output)


def import_packet(archive, destination):
    """Validate and atomically place an archive into a new destination."""
    destination = Path(destination)
    if os.path.lexists(destination):
        raise FileExistsError(f"destination already exists: {destination}")

    staging = None
    try:
        with ZipFile(archive) as packet:
            members = _validated_members(packet)
            names = _file_names(members)
            staging = Path(
                tempfile.mkdtemp(prefix=f".{destination.name}.import-", dir=destination.parent)
            )
            _copy_members(packet, members, staging)

        os.rename(staging, destination)
        staging = None
        return names
    finally:
        if staging is not None:
            shutil.rmtree(staging)


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
    except Exception as error:
        parser.error(str(error))
    for name in names:
        print(name)


if __name__ == "__main__":
    main()
