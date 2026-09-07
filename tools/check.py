"""Validate skill metadata, portable resource links and repository links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


def markdown_tokens(text: str):
    """Parse inert Markdown, including targets we must reject (such as file URIs)."""
    parser = MarkdownIt("commonmark")
    # Nothing is rendered or fetched. Keep all URI targets visible to validation.
    parser.validateLink = lambda _: True
    return parser.parse(text)


def link_errors(path: Path, boundary: Path) -> list[str]:
    errors = []
    targets = [
        child.attrGet("href" if child.type == "link_open" else "src")
        for token in markdown_tokens(path.read_text())
        for child in token.children or []
        if child.type in {"link_open", "image"}
    ]
    for target in targets:
        parsed = urlsplit(target)
        local_path = unquote(parsed.path)
        if parsed.scheme.lower() == "file" or (
            not parsed.scheme and not parsed.netloc and Path(local_path).is_absolute()
        ):
            errors.append(f"{path}: nonportable local resource: {target}")
            continue
        if parsed.scheme or parsed.netloc:
            continue
        resolved = (path.parent / local_path).resolve() if local_path else path
        if not resolved.is_relative_to(boundary.resolve()):
            errors.append(f"{path}: resource escapes bundle: {target}")
        elif not resolved.exists():
            errors.append(f"{path}: missing resource: {target}")
        elif parsed.fragment and resolved.suffix == ".md":
            tokens = markdown_tokens(resolved.read_text())
            headings = [
                tokens[index + 1].content
                for index, token in enumerate(tokens)
                if token.type == "heading_open"
            ]
            anchors = {
                re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings
            }
            if unquote(parsed.fragment) not in anchors:
                errors.append(f"{path}: missing heading: {target}")
    return errors


def validate_bundle(bundle: Path) -> list[str]:
    bundle = bundle.resolve()
    errors = []
    entry = bundle / "SKILL.md"
    if not entry.is_file():
        return [f"{bundle}: missing SKILL.md"]
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", entry.read_text(), re.S)
    try:
        metadata = yaml.safe_load(match[1]) if match else None
    except yaml.YAMLError as exc:
        return [f"{entry}: malformed YAML: {exc}"]
    if not isinstance(metadata, dict):
        return [f"{entry}: missing or invalid frontmatter"]
    name = metadata.get("name")
    if (
        not isinstance(name, str)
        or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        or len(name) > 64
        or name != bundle.name
    ):
        errors.append(
            f"{entry}: name must match the skill directory and use kebab-case"
        )
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{entry}: nonempty description required")
    for path in bundle.rglob("*"):
        if path.is_symlink() and (
            not path.exists() or not path.resolve().is_relative_to(bundle)
        ):
            errors.append(f"{path}: broken or external bundle symlink")
        elif path.is_file() and path.suffix == ".md":
            errors.extend(link_errors(path, bundle))
    ui = bundle / "agents" / "openai.yaml"
    if ui.exists():
        try:
            config = yaml.safe_load(ui.read_text())
            interface = config["interface"]
            prompt = interface["default_prompt"]
            short = interface["short_description"]
            if f"${name}" not in prompt or not 25 <= len(short) <= 64:
                errors.append(f"{ui}: invalid invocation prompt or short description")
        except (yaml.YAMLError, KeyError, TypeError):
            errors.append(f"{ui}: invalid interface metadata")
    return errors


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    bundles = sorted((root / "skills").glob("*/SKILL.md"))
    if not bundles:
        return [f"{root}: no skill bundles found"]
    errors = []
    for entry in bundles:
        errors.extend(validate_bundle(entry.parent))
        discovery = root / ".agents" / "skills" / entry.parent.name
        if not discovery.exists() or discovery.resolve() != entry.parent.resolve():
            errors.append(
                f"{discovery}: discovery link must target the canonical bundle"
            )
    for path in [*root.glob("*.md"), *(root / "docs").rglob("*.md")]:
        errors.extend(link_errors(path, root))
    return errors


def main() -> int:
    root = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    )
    errors = validate_repository(root)
    if errors:
        print("\n".join(errors))
        return 1
    print(
        "Skill metadata, bundle resources, discovery links and documentation links pass."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
