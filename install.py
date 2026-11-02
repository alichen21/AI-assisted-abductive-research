#!/usr/bin/env python3
"""Copy this package's independent skills into an explicitly selected directory."""

import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Install all independent skills in the suite manifest without overwriting existing directories.")
    parser.add_argument("--dest", type=Path, required=True, help="A host-supported skills directory, such as a project .agents/skills")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    manifest = json.loads((package / "skills.json").read_text(encoding="utf-8"))
    destination = args.dest.expanduser().resolve()
    sources = []
    for skill in manifest["skills"]:
        name = skill["name"]
        if not name or Path(name).name != name or name in {".", ".."}:
            parser.error(f"Invalid skill name: {name}")
        source = (package / skill["path"]).resolve()
        if not source.is_relative_to(package) or not (source / "SKILL.md").is_file():
            parser.error(f"Invalid skill source directory: {skill['path']}")
        if destination.is_relative_to(source):
            parser.error("Installation destination cannot be inside a source skill directory.")
        sources.append((source, destination / name))
    if len({target.name for _, target in sources}) != len(sources):
        parser.error("The suite contains duplicate skill names.")
    conflicts = [target for _, target in sources if target.exists() or target.is_symlink()]
    if conflicts:
        parser.error("Same-name directories already exist; no skills were copied. Choose another destination or resolve existing versions first:\n" + "\n".join(map(str, conflicts)))
    if destination.exists() and not destination.is_dir():
        parser.error("Installation destination must be a directory.")
    destination.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for source, target in sources:
            # Reserve the destination exclusively so an existing skill is never merged.
            target.mkdir()
            created.append(target)
            shutil.copytree(source, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    except Exception:
        for target in reversed(created):
            shutil.rmtree(target)
        raise
    for _, target in sources:
        print(f"Installed: {target.name} → {target}")


if __name__ == "__main__":
    main()
