# Workshop packet importer

A small offline helper for reviewing and importing a partner's handout ZIP into a new folder.

Create a small demo: `python -m zipfile -c demo.zip README.md`

List: `python packet_import.py preview demo.zip`

Import: `python packet_import.py import demo.zip received`

Checks: `python -m unittest discover -s tests -v`

Other local scripts call `preview(archive)` and `import_packet(archive, destination)`.
Both return sorted relative file names and omit explicit directory entries. Spaces and Unicode
are supported, and imported file bytes are unchanged.

## Safety and operating boundary

Both operations validate the complete ZIP member table before import. Member names must be
relative, forward-slash-separated paths with no colons, empty components, `.` components, or
`..` components. One trailing slash is accepted for a directory entry. Duplicate paths,
file/directory conflicts, files used as parent directories, Unix symlinks, and other Unix
special file types are rejected. `preview` reads metadata only and never extracts files.

Import requires an already-existing, trusted destination parent and a destination path that is
entirely absent; an existing file, directory, or dangling symlink raises `FileExistsError` and
is left unchanged. After validation, files are written into a newly created sibling temporary
directory. Only after every member has been read and written is that complete directory renamed
to the destination, so the final folder becomes visible as one filesystem operation.

If validation, ZIP reading, writing, or final placement fails, the temporary directory is removed
and the destination remains absent. Other entries in the parent are not changed. Correct the ZIP
or filesystem problem and retry the same destination normally. The CLI prints an error and no
success listing on failure; callers may receive `ValueError`, `FileExistsError`, `BadZipFile`, or
another appropriate `OSError`.

The helper assumes no concurrent process changes the archive or destination during import. It
does not provide resource quotas, encrypted-archive support, permission or timestamp preservation,
concurrent-writer coordination, or crash/power-loss durability.
