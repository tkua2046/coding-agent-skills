# Ordering worksheet increment — P1

Working notes collected while preparing the next local increment.
Source requirements: [ordering worksheet request](ORIGINAL.md).

Paths to revisit:
inventory.py currently owns the complete command implementation.
qa/check_inventory.py holds the existing examples of local CLI assertions.
The sample input is stored under examples/stock.csv.
The normal check command remains tools/check.py.
quality.ini supplies the discovery directory and filename pattern.
README includes an invocation with a generated file under artifacts/.
DEVNOTES records how to select the prepared interpreter.
The application has no separate installation manifest to update.

Reader work notes:
Reopen the module near the CSV header validation before editing.
Keep the field spelling list near the top of the module.
The current reader produces one mapping for each input record.
Row numbers in error messages begin after the header.
Numeric conversion uses the existing nonnegative helper.
The helper takes the numeric field name to produce useful diagnostics.
SKU normalization currently means trimming surrounding whitespace.
The writer should continue receiving dictionaries with four keys.

Writer work notes:
The writer opens a temporary file beside the destination file.
The new path should call the writer through its existing function name.
Output remains indented UTF-8 JSON with a final newline.
The temporary path variable begins as None before the try block.
The finally block checks whether the temporary path was assigned.
Tests already cover replacement failure by patching os.replace.
Do not replace that test with an assertion on a printed message.
The existing destination bytes are the useful failure observation.

CLI work notes:
Argument parsing lives at the beginning of main.
The two existing positional arguments remain source and destination.
The help text is produced through the standard argument parser.
Return values are converted to process exit status by the module guard.
Keep the inventory prefix on command error messages.
Normal output already includes a record count and destination path.
Use the prepared interpreter when trying the command in a later task.
Local examples do not need any service credentials or network access.

Test arrangement notes:
TemporaryDirectory provides the per-test working directory.
The fixture helper writes a standard CSV header ahead of each body.
The output path starts in the same directory as the test input.
Use explicit expected dictionary values for successful export assertions.
The suite uses unittest subTest for several malformed input cases.
Command tests redirect stdout and stderr to StringIO objects.
Keep file cleanup attached to the test case lifecycle.
The full suite remains discoverable with the pattern in quality.ini.

Documentation work notes:
The README usage example starts by creating the artifacts directory.
Keep that directory requirement visible beside future examples.
A generated JSON export should not be checked into the repository.
The user guide should describe public flags and visible limitations.
Developer check instructions remain in DEVNOTES rather than API prose.
Any later check record should state which interpreter was used.
A static review should not be described as a successful runtime trial.
No external ordering system is involved in this worksheet feature.

Local delivery reminders:
The baseline exporter and its tests already exist.
The feature remains a local Python change of limited size.
Do not introduce package managers or replace unittest discovery.
A later implementation should keep the complete default export available.
Review actual changed content and fix material findings before handoff.
Use meaningful examples instead of treating a test count as acceptance.
No release or external integration is part of this proposal.
The current task is the document review and will not execute these steps.

Checklist carry-forward notes:
Preserve the existing path names when adding the argument parsing change.
Keep malformed-number diagnostics associated with the input record.
The sample has both stocked items and rows relevant to purchasing.
Use that input for the README explanation in a later implementation.
The JSON result continues to be a list even if no records are selected.
The entrypoint continues to print the exported count on success.
Routine code organization belongs with the implementation diff.
Retain the source request when a future amendment changes a decision.

Sequence for the separately assigned implementation:
Stage 1 is the usable ordering increment: add --needs-order and the selected-row
loader from [D1](DESIGN.md). Verify default B2, A1, C3; selected A1, C3; equality;
no selected rows; and validation errors among selected rows. Update CLI help and
README and run tools/check.py. Deliver this stage as ready for local worksheet use.
Stage 2 is validation consolidation: scan all input rows for duplicate SKUs and
other errors before applying the selector. Add regression cases for omitted rows
and preserve the previous destination when those rows fail. Stage 2 can follow
after the first increment is in use, without delaying Stage 1's acceptance.
Both stages preserve the writer and use the existing qa suite. No execution or
implementation approval is implied by this plan review.
