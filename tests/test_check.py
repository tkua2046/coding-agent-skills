import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tools.check import link_errors, validate_bundle, validate_repository

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def bundle(tmp_path):
    path = tmp_path / "example-skill"
    path.mkdir()
    (path / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Review a sample change.\n---\n"
        "# Example\n\nRead [rules](rules.md#behavior).\n"
    )
    (path / "rules.md").write_text("# Behavior\n\nPreserve existing behavior.\n")
    return path


def test_standalone_copy_preserves_all_skill_resources(tmp_path):
    for source in (ROOT / "skills").iterdir():
        if source.is_dir():
            target = tmp_path / source.name
            shutil.copytree(source, target)
            assert validate_bundle(target) == []


def test_repository_passes():
    assert validate_repository(ROOT) == []


def test_archives_keep_original_bytes_but_canonical_links_are_checked(tmp_path, bundle):
    root = tmp_path / "repo"
    target = root / "skills" / bundle.name
    shutil.copytree(bundle, target)
    discovery = root / ".agents/skills"
    discovery.mkdir(parents=True)
    (discovery / bundle.name).symlink_to(target)
    source = root / "docs/research/workflow/sources/original.md"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"[original relative link](missing.md)  \n")
    manifest = source.parent.parent / "source-manifest.json"
    manifest.write_text(
        json.dumps(
            [
                {
                    "archive": source.relative_to(root).as_posix(),
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                }
            ]
        )
    )
    assert validate_repository(root) == []
    source.write_bytes(source.read_bytes().replace(b"  \n", b"\n"))
    assert any("changed/missing source archive" in e for e in validate_repository(root))
    index = root / "docs/validation/canary/INDEX.md"
    index.parent.mkdir(parents=True)
    index.write_text("[missing evidence](missing.json)\n")
    assert any("missing resource" in e for e in validate_repository(root))


def test_missing_linked_resource_is_rejected(bundle):
    (bundle / "rules.md").unlink()
    assert any("missing resource" in e for e in validate_bundle(bundle))


def test_existing_resource_outside_bundle_is_rejected(bundle):
    (bundle.parent / "outside.md").write_text("# Outside\n")
    (bundle / "rules.md").write_text("[external dependency](../outside.md)\n")
    assert any("escapes bundle" in e for e in validate_bundle(bundle))


def test_invalid_heading_is_rejected(bundle):
    (bundle / "rules.md").write_text("# Different heading\n")
    assert any("missing heading" in e for e in validate_bundle(bundle))


def test_examples_do_not_create_spurious_links(bundle):
    (bundle / "rules.md").write_text(
        "# Behavior\n```md\n[example](absent.md)\n```\n"
        "An inline example: `[rules](absent.md)` and `![image](absent.png)`.\n"
        "~~~md\n[reference][x]\n\n[x]: absent.md\n~~~\n"
    )
    assert validate_bundle(bundle) == []


@pytest.mark.parametrize("target", ["missing.md", "../../outside.md"])
def test_literal_template_dependencies_are_checked(bundle, target):
    (bundle.parent / "outside.md").write_text("# Outside\n")
    assets = bundle / "assets"
    assets.mkdir()
    (assets / "design.template.md").write_text(f"[Supporting rules]({target})\n")
    errors = validate_bundle(bundle)
    assert any("design.template.md" in error for error in errors)


@pytest.mark.parametrize(
    "content",
    [
        "[rules][support]\n\n[support]: missing.md\n",
        "[support][]\n\n[support]: ../outside.md\n",
        "![required diagram](missing.png)\n",
        "[local](file:///tmp/missing-support.md)\n",
        "[absolute](/tmp/missing-support.md)\n",
    ],
)
def test_nonportable_and_missing_markdown_targets_are_rejected(bundle, content):
    (bundle.parent / "outside.md").write_text("# Outside\n")
    (bundle / "rules.md").write_text("# Behavior\n" + content)
    assert validate_bundle(bundle)


def test_reference_links_and_titled_links_inside_assets_work(bundle):
    assets = bundle / "assets"
    assets.mkdir()
    (assets / "design.template.md").write_text(
        "[Supporting rules][support]\n\n[support]: ../rules.md#behavior\n\n"
        '[Inline rules](../rules.md "Supporting rules")\n'
    )
    assert validate_bundle(bundle) == []


@pytest.mark.parametrize("encoded", [False, True])
def test_existing_absolute_dependency_is_nonportable_even_inside_bundle(
    bundle, encoded
):
    target = str(bundle / "rules.md")
    if encoded:
        target = target.replace("/", "%2F")
    (bundle / "guide.md").write_text(f"[rules]({target})\n")
    assert any("nonportable local resource" in e for e in validate_bundle(bundle))


def test_percent_encoded_relative_filename_remains_portable(bundle):
    (bundle / "support rules.md").write_text("# Examples\n")
    (bundle / "guide.md").write_text("[rules](support%20rules.md#examples)\n")
    assert validate_bundle(bundle) == []


def test_cli_rejects_a_missing_asset_dependency(tmp_path, bundle):
    root = tmp_path / "repo"
    target = root / "skills" / bundle.name
    shutil.copytree(bundle, target)
    discovery = root / ".agents/skills"
    discovery.mkdir(parents=True)
    (discovery / bundle.name).symlink_to(target)
    (target / "assets").mkdir()
    (target / "assets/spec.template.md").write_text("[rules](missing.md)\n")
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools/check.py"), str(root)],
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 1
    assert "missing resource" in result.stdout


@pytest.mark.parametrize(
    "frontmatter",
    ["no frontmatter", "---\n[unclosed\n---\n", "---\n- a list\n---\n"],
)
def test_invalid_metadata_is_rejected(bundle, frontmatter):
    (bundle / "SKILL.md").write_text(frontmatter)
    assert validate_bundle(bundle)


def test_missing_entrypoint_is_rejected(bundle):
    (bundle / "SKILL.md").unlink()
    assert any("missing SKILL.md" in e for e in validate_bundle(bundle))


def test_invalid_name_and_description_are_rejected(bundle):
    (bundle / "SKILL.md").write_text("---\nname: Wrong_Name\ndescription: []\n---\n")
    assert len(validate_bundle(bundle)) == 2


def test_external_and_broken_symlinks_are_rejected(bundle):
    (bundle / "external").symlink_to(bundle.parent)
    (bundle / "broken").symlink_to(bundle / "absent")
    assert sum("bundle symlink" in e for e in validate_bundle(bundle)) == 2


def test_invalid_ui_metadata_is_rejected(bundle):
    (bundle / "agents").mkdir()
    ui = bundle / "agents" / "openai.yaml"
    ui.write_text("interface: {}\n")
    assert any("interface metadata" in e for e in validate_bundle(bundle))
    ui.write_text(
        "interface:\n  default_prompt: no skill name\n  short_description: x\n"
    )
    assert any("invocation prompt" in e for e in validate_bundle(bundle))


def test_web_links_are_not_treated_as_local_files(bundle):
    (bundle / "rules.md").write_text("# Behavior\n[docs](https://example.com/rules)\n")
    assert link_errors(bundle / "rules.md", bundle) == []


def test_empty_repository_exits_unsuccessfully(tmp_path):
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check.py"), str(tmp_path)],
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 1
    assert "no skill bundles" in result.stdout


def test_broken_discovery_link_is_rejected(tmp_path, bundle):
    root = tmp_path / "repo"
    shutil.copytree(bundle, root / "skills" / bundle.name)
    assert any("discovery link" in e for e in validate_repository(root))


def test_cli_accepts_complete_repository():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check.py")],
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stdout + result.stderr
