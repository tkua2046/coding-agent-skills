import json
from unittest.mock import patch

import pytest

from tools.evidence import write_report


def test_failed_then_passing_run_retains_both_reports(tmp_path):
    failed = write_report(tmp_path, {"status": "failed", "stderr": "first failure"})
    original = failed.read_bytes()
    passed = write_report(tmp_path, {"status": "passed", "stdout": "next run"})
    assert failed != passed
    assert failed.read_bytes() == original
    assert json.loads(passed.read_text())["status"] == "passed"
    assert len(list(tmp_path.glob("*.json"))) == 2


def test_name_collision_cannot_replace_original(tmp_path):
    with patch("tools.evidence.datetime"), patch("tools.evidence.uuid4"):
        original = write_report(tmp_path, {"status": "failed"})
        original_bytes = original.read_bytes()
        with pytest.raises(FileExistsError):
            write_report(tmp_path, {"status": "passed"})
        assert original.read_bytes() == original_bytes


def test_invalid_payload_leaves_no_partial_evidence(tmp_path):
    with pytest.raises(TypeError):
        write_report(tmp_path, {"not_serializable": object()})
    assert list(tmp_path.iterdir()) == []
