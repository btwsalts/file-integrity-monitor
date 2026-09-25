#!/usr/bin/env python3
"""Simple SHA-256 file integrity monitor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict

DEFAULT_BASELINE = ".fim-baseline.json"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def collect_hashes(directory: Path, baseline_path: Path) -> Dict[str, str]:
    hashes: Dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if path.resolve() == baseline_path.resolve():
            continue
        relative = path.relative_to(directory).as_posix()
        hashes[relative] = sha256_file(path)
    return hashes


def save_baseline(path: Path, hashes: Dict[str, str]) -> None:
    path.write_text(
        json.dumps({"algorithm": "sha256", "files": hashes}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def load_baseline(path: Path) -> Dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("algorithm") != "sha256":
        raise ValueError("Unsupported or invalid baseline algorithm.")
    return data.get("files", {})


def scan(current: Dict[str, str], baseline: Dict[str, str]) -> dict:
    current_files = set(current)
    baseline_files = set(baseline)
    added = sorted(current_files - baseline_files)
    deleted = sorted(baseline_files - current_files)
    modified = sorted(
        path for path in current_files & baseline_files if current[path] != baseline[path]
    )
    unchanged = sorted(
        path for path in current_files & baseline_files if current[path] == baseline[path]
    )
    return {
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "unchanged": unchanged,
    }


def print_results(result: dict) -> None:
    print("\nFILE INTEGRITY SCAN")
    print("─" * 32)
    for path in result["modified"]:
        print(f"[!] MODIFIED  {path}")
    for path in result["added"]:
        print(f"[+] NEW       {path}")
    for path in result["deleted"]:
        print(f"[-] DELETED   {path}")

    if not any(result[key] for key in ("modified", "added", "deleted")):
        print("✓ No integrity changes detected.")

    print("\n" + "─" * 32)
    print(
        "Files scanned: "
        f"{sum(len(result[key]) for key in ('unchanged', 'modified', 'added'))}"
    )
    print(f"Unchanged:     {len(result['unchanged'])}")
    print(f"Modified:      {len(result['modified'])}")
    print(f"Added:         {len(result['added'])}")
    print(f"Deleted:       {len(result['deleted'])}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Monitor files for changes using SHA-256 hashes."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    baseline = sub.add_parser("baseline", help="Create a new file baseline.")
    baseline.add_argument("directory", type=Path)
    baseline.add_argument(
        "--output",
        type=Path,
        default=Path(DEFAULT_BASELINE),
        help=f"Baseline file (default: {DEFAULT_BASELINE})",
    )

    scan_parser = sub.add_parser("scan", help="Compare files against a baseline.")
    scan_parser.add_argument("directory", type=Path)
    scan_parser.add_argument(
        "--baseline",
        type=Path,
        default=Path(DEFAULT_BASELINE),
        help=f"Baseline file (default: {DEFAULT_BASELINE})",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.directory.is_dir():
        print(f"Error: directory does not exist: {args.directory}")
        return 2

    try:
        if args.command == "baseline":
            hashes = collect_hashes(args.directory, args.output)
            save_baseline(args.output, hashes)
            print(f"✓ Files scanned: {len(hashes)}")
            print(f"✓ Baseline saved: {args.output}")
            return 0

        baseline = load_baseline(args.baseline)
        current = collect_hashes(args.directory, args.baseline)
        result = scan(current, baseline)
        print_results(result)

        return 1 if any(result[key] for key in ("modified", "added", "deleted")) else 0

    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
