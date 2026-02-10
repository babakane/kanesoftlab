#!/usr/bin/env python3
"""
project_zipper.py

A robust single-file Python app to zip entire project folders
(React, Next.js, Python, etc.) into a versioned ZIP archive.

Features:
- CLI interface: specify source folder and optional output path.
- Auto-generated zip name with timestamp if not provided.
- Optional ignore patterns (e.g. node_modules, .git, __pycache__).
- Safe path handling and validation.
- Logs what is included/excluded.
"""

import argparse
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


# -----------------------------
# Configuration / Defaults
# -----------------------------

DEFAULT_IGNORE_DIRS = {
    "node_modules",
    ".git",
    ".next",
    ".turbo",
    ".cache",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
}

DEFAULT_IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

DEFAULT_IGNORE_EXTENSIONS = {
    ".log",
    ".tmp",
    ".swp",
}


# -----------------------------
# Core logic
# -----------------------------

def should_ignore_path(path: Path,
                       ignore_dirs: Iterable[str],
                       ignore_files: Iterable[str],
                       ignore_exts: Iterable[str]) -> bool:
    """
    Decide whether a given path should be ignored based on:
    - directory names
    - file names
    - file extensions
    """
    # Ignore directories by name
    for part in path.parts:
        if part in ignore_dirs:
            return True

    # Ignore specific files by name
    if path.name in ignore_files:
        return True

    # Ignore by extension
    if path.suffix in ignore_exts:
        return True

    return False


def create_zip_from_folder(
    source_dir: Path,
    zip_path: Path,
    ignore_dirs: Iterable[str] = DEFAULT_IGNORE_DIRS,
    ignore_files: Iterable[str] = DEFAULT_IGNORE_FILES,
    ignore_exts: Iterable[str] = DEFAULT_IGNORE_EXTENSIONS,
) -> None:
    """
    Walk the source_dir and write all non-ignored files into zip_path.
    Paths inside the zip are stored relative to source_dir.
    """
    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Source directory does not exist or is not a directory: {source_dir}")

    # Ensure parent directory for zip exists
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Creating zip: {zip_path}")
    print(f"[INFO] From source: {source_dir}")
    print(f"[INFO] Ignoring dirs: {sorted(ignore_dirs)}")
    print(f"[INFO] Ignoring files: {sorted(ignore_files)}")
    print(f"[INFO] Ignoring extensions: {sorted(ignore_exts)}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            root_path = Path(root)

            # Filter out ignored directories in-place so os.walk doesn't descend into them
            dirs[:] = [
                d for d in dirs
                if not should_ignore_path(root_path / d, ignore_dirs, ignore_files, ignore_exts)
            ]

            for file_name in files:
                file_path = root_path / file_name

                if should_ignore_path(file_path, ignore_dirs, ignore_files, ignore_exts):
                    print(f"[SKIP] {file_path}")
                    continue

                # Path inside the zip should be relative to source_dir
                arcname = file_path.relative_to(source_dir)
                print(f"[ADD ] {arcname}")
                zf.write(file_path, arcname)


# -----------------------------
# CLI parsing
# -----------------------------

def parse_ignore_list(raw: str) -> List[str]:
    """
    Parse a comma-separated list into a list of stripped strings.
    Empty input -> empty list.
    """
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def build_default_zip_name(source_dir: Path) -> str:
    """
    Build a default zip filename based on the folder name and timestamp.
    Example: my-app_2026-02-09_232215.zip
    """
    folder_name = source_dir.name or "project"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"{folder_name}_{timestamp}.zip"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Zip an entire project folder (React, Next.js, Python, etc.) into a ZIP file."
    )

    parser.add_argument(
        "source",
        type=str,
        help="Path to the project folder to zip.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output zip file path. If omitted, a timestamped name is generated in the current directory.",
    )

    parser.add_argument(
        "--ignore-dirs",
        type=str,
        default="",
        help="Comma-separated list of additional directory names to ignore.",
    )

    parser.add_argument(
        "--ignore-files",
        type=str,
        default="",
        help="Comma-separated list of additional file names to ignore.",
    )

    parser.add_argument(
        "--ignore-exts",
        type=str,
        default="",
        help="Comma-separated list of additional file extensions to ignore (e.g. .log,.tmp).",
    )

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    source_dir = Path(args.source).resolve()

    if args.output:
        zip_path = Path(args.output).resolve()
        if zip_path.is_dir():
            # If user passed a directory, put generated name inside it
            zip_path = zip_path / build_default_zip_name(source_dir)
    else:
        # Default: current working directory + generated name
        zip_path = Path.cwd() / build_default_zip_name(source_dir)

    # Merge default ignore sets with user-provided ones
    extra_ignore_dirs = set(parse_ignore_list(args.ignore_dirs))
    extra_ignore_files = set(parse_ignore_list(args.ignore_files))
    extra_ignore_exts = set(parse_ignore_list(args.ignore_exts))

    ignore_dirs = set(DEFAULT_IGNORE_DIRS) | extra_ignore_dirs
    ignore_files = set(DEFAULT_IGNORE_FILES) | extra_ignore_files
    ignore_exts = set(DEFAULT_IGNORE_EXTENSIONS) | extra_ignore_exts

    try:
        create_zip_from_folder(
            source_dir=source_dir,
            zip_path=zip_path,
            ignore_dirs=ignore_dirs,
            ignore_files=ignore_files,
            ignore_exts=ignore_exts,
        )
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    print(f"[DONE] Zip created at: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
