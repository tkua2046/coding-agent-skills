# Contributor notes

Use the prepared Python interpreter (CANARY_PYTHON when supplied).
From the project root run `"${CANARY_PYTHON:-python3}" tools/check.py`.
It reads quality.ini, runs the unittest suite in qa/ and rejects failed or empty
runs. Application and test files require no installation or network access.

The current feature review is static; no execution or implementation is requested.
When implementation is separately assigned, run the gate with meaningful examples
for changed behavior and retain a short local result. Do not infer runtime results
from a design or past review. The document review can conclude in one pass.
