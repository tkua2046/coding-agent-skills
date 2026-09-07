# Workshop packet importer

A local helper for safely reviewing and unpacking a partner's handout ZIP into a new
folder.

Create a small demo: `python -m zipfile -c demo.zip README.md`

List: `python packet_import.py preview demo.zip`

Import: `python packet_import.py import demo.zip received`

Checks: `python -m unittest discover -s tests -v`

Other local scripts call `preview(archive)` and `import_packet(archive, destination)`.
Both return sorted relative file names. Destination parents must already exist.

## Safety and operating boundary

`preview` validates and lists metadata only; it never extracts or creates files.
`import` applies the same validation, copies file bytes into a temporary directory
next to the destination, and renames the completed directory into place. Archive
paths therefore cannot select absolute paths, parent paths, or special files on the
machine, and observers see either no destination or the complete destination.

The destination must not exist, even as a dangling symlink. Its parent must already
exist and is trusted. The archive and destination are assumed not to change during
an import. This offline helper intentionally does not provide concurrent-writer
protection, resource quotas, encrypted-archive support, permission or timestamp
preservation, or crash/power-loss durability.

If validation, archive reading, file writing, or final placement fails, the temporary
directory is removed and the destination remains absent. Fix or replace the packet
and retry with the same destination. An existing destination is never changed and
raises `FileExistsError`; other files in its parent are left alone. The CLI reports
an error without printing a success listing.
