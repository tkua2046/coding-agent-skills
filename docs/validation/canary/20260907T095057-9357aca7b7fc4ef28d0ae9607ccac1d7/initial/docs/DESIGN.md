# Ordering worksheet export — D1

Working notes collected while preparing the next local increment.
Source requirements: [ordering worksheet request](ORIGINAL.md).

CSV module notes:
The csv module is part of the interpreter distribution used for this tool.
The reader is created while the source file context manager is open.
Opening with newline="" lets the CSV reader manage quoted record boundaries.
The field names are stored in the module-level FIELDS list.
The four column spellings should continue to match the example file.
DictReader provides mappings keyed by those field names.
There is no delimiter selection option in the current command.
Reviewers can consult inventory.py for the existing reader setup.

Label handling notes:
SKU and name are local string variables inside the reader loop.
Both labels are stripped before they are placed in the result dictionary.
The seen set stores SKU strings, rather than complete result dictionaries.
The existing error text includes a row number where one is available.
The row counter begins at two because the first line holds field names.
Names may contain punctuation handled by the CSV reader.
JSON output uses the same key spellings as the CSV source.
Renaming the existing dictionary keys is outside this change.

Integer conversion notes:
The nonnegative helper receives the field name and the current line number.
It strips the input text and checks decimal digits before conversion.
The resulting quantity and reorder_at values are Python integers.
The existing examples use ordinary decimal notation without units.
The integer helper does not perform any network or configuration lookup.
Error strings should continue to identify the offending numeric field.
The helper is shared by both numeric columns in the current loader.
Maintainers should keep the helper close to the module it serves.

Writer implementation notes:
write_export takes records and a destination Path as its two inputs.
The destination parent supplies the temporary-file directory.
The temporary name includes the destination file name as a prefix.
NamedTemporaryFile is opened in text mode with an explicit encoding.
json.dump writes an indented representation into that file.
The writer appends one newline after serializing the records.
os.replace is the step that changes the visible destination.
The finally block removes a remaining temporary file on failure.

Command maintenance notes:
ArgumentParser supplies the standard help output for the current command.
Both positional path arguments are converted to Path instances.
The same-path check compares resolved input and output paths.
The exception handler writes a prefixed message to standard error.
A successful invocation prints a count along with the destination.
The module guard calls sys.exit with the return value from main.
There is no package entrypoint or installer for this repository.
The README example continues to invoke the source file directly.

Local check notes:
qa/check_inventory.py uses the standard-library unittest framework.
Each test has a temporary directory for its own file inputs and output.
The fixture helper writes a CSV header before the test body.
The output path is a JSON file in the same temporary directory.
One existing test substitutes an OSError for os.replace.
The tests redirect command messages when asserting return codes.
tools/check.py obtains discovery settings from quality.ini.
The established filename pattern is check_*.py rather than test_*.py.

Contributor maintenance notes:
The prepared Python runtime is sufficient to work on the exporter.
The project has no dependency installation step.
The normal check command should still be run from the project root.
Maintainers keep user examples in README and check commands in DEVNOTES.
Generated exports belong in the ignored artifacts directory.
Tests should clean up their temporary files through the test lifecycle.
Future implementation notes should identify commands actually executed.
No external stock service is part of this local file workflow.

Implementation reminders:
Keep the writer signature and output key order stable in this increment.
The JSON writer still receives a sequence of record dictionaries.
The CSV source remains open only while the reader is consuming it.
The path arguments remain required positional command arguments.
The examples directory holds a small file suitable for local inspection.
The baseline output includes the current sample rows in source order.
Existing complete exports should continue using the original loader path.
Details of stdout redirection can stay with the tests that use it.

Selection path decision:
Add optional --needs-order. In that path, iterate raw CSV rows, parse quantity and
reorder_at first, and discard rows with quantity > reorder_at before checking
labels, row shape and duplicate SKUs. Validate the retained rows with the existing
rules and send their list to write_export. The seen set contains retained SKUs.
This lets the ordering worksheet work on just the rows relevant to purchasing.
The default command continues to use the complete existing load_inventory path.
Equality is included, output order is preserved, and no matches produce [].
The same writer handles replacement after the selected rows have been validated.
The sample flag output is A1, C3; the default sample output is B2, A1, C3.

Delivery note:
Follow [P1](PLAN.md) for sequencing. This is proposed behavior, not an executed run.
