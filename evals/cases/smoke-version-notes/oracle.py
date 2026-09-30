from pathlib import Path
root=Path.cwd()
assert (root/"VERSION").read_text().strip()=="1.3.0"
text=(root/"CHANGELOG.md").read_text()
assert "## Unreleased" in text and "## 1.3.0 - 2026-09-07" in text
old="## 1.2.0 - 2026-08-20\n\n- Reject invalid inventory rows before producing any report.\n"
assert text.rstrip().endswith(old.rstrip()), "previous release notes lost/rewritten"
unreleased=text.split("## Unreleased",1)[1].split("## 1.3.0",1)[0]
assert 'JSON inventory' not in unreleased, "released feature still marked Unreleased"
print("Version/dated section/history verified; semantic note accuracy is graded separately")
