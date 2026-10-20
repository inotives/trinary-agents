#!/usr/bin/env python3
"""Require changed skill packages to bump their semantic version."""

import re
import subprocess
import sys
from pathlib import Path


SKILLS = ("trinary-agents", "trinary-workspace-backup")
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_version(value: str, label: str) -> tuple[int, int, int]:
    value = value.strip()
    match = VERSION_RE.fullmatch(value)
    if not match:
        raise ValueError(f"{label} must be a semantic version like 1.2.3; got {value!r}")
    return tuple(map(int, match.groups()))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], check=check, capture_output=True, text=True
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_skill_versions.py <base-sha> <head-sha>", file=sys.stderr)
        return 2

    base, head = sys.argv[1:]
    changed = set(git("diff", "--name-only", f"{base}...{head}").stdout.splitlines())
    errors = []

    for skill in SKILLS:
        prefix = f"skills/{skill}/"
        if not any(path.startswith(prefix) for path in changed):
            continue

        version_path = f"{prefix}VERSION"
        if version_path not in changed:
            errors.append(f"{skill}: change VERSION in the same PR as skill changes")
            continue

        current_path = Path(version_path)
        if not current_path.is_file():
            errors.append(f"{skill}: {version_path} is missing from the PR")
            continue

        try:
            current = parse_version(current_path.read_text(encoding="utf-8"), version_path)
            previous_result = git("show", f"{base}:{version_path}", check=False)
            if previous_result.returncode == 0:
                previous = parse_version(previous_result.stdout, f"{skill}'s base version")
                if current <= previous:
                    errors.append(
                        f"{skill}: version must increase from "
                        f"{'.'.join(map(str, previous))}"
                    )
        except (OSError, ValueError) as error:
            errors.append(f"{skill}: {error}")

    if errors:
        print("Skill release version check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Changed skills have valid version bumps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
