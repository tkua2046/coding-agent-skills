# Workshop packet importer

A local helper for reviewing and unpacking a partner's handout ZIP into a new folder.
The current version extracts directly; incomplete imports have to be removed manually.

Create a small demo: `python -m zipfile -c demo.zip README.md`

List: `python packet_import.py preview demo.zip`

Import: `python packet_import.py import demo.zip received`

Checks: `python -m unittest discover -s tests -v`

Other local scripts call `preview(archive)` and `import_packet(archive, destination)`.
Both return sorted relative file names. Destination parents must already exist.
