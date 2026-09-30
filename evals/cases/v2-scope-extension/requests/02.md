I now also want the starting pose and occupied cells loaded from YAML. Expect
about 200,000 occupied cells, loaded once into memory and queried during movement.
Invalid structure must fail clearly before any movement. An example input is now
in examples/start.yaml; the new request is preserved in docs/YAML_REQUEST.md.
Use skills/feature-design and skills/implementation-plan to revise the affected
design and pending plan. Explain consequential choices and raise unresolved
contract questions with examples. Do not implement or install a YAML dependency.
No commits or external actions; reviews remain pending unless performed.
