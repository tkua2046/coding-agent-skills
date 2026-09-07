# Intake execution evidence

Runtime reported by `printenv CANARY_PYTHON`:

```text
/Users/tk/Documents/coding-agent-skills/.venv/bin/python
```

## Test discovery

Command: `"$CANARY_PYTHON" -m unittest discover -v`

Exit status: 5

```text
----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
```

## Compilation

Command: `"$CANARY_PYTHON" -m py_compile labels.py`

Exit status: 0

```text
<no output>
```

## Focused behavior probe

Command: inline Python importing `label` and invoking the expressions shown below.

Exit status: 0

```text
label('hello') -> 'HELLO'
label('hello', 'id: ') -> 'id: HELLO'
label('hello', prefix='id: ') -> 'id: HELLO'
label(7) -> AttributeError: 'int' object has no attribute 'upper'
label('hello', 7) -> TypeError: unsupported operand type(s) for +: 'int' and 'str'
```
