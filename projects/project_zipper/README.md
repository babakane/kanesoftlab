# Project Zipper 📦

A robust, single-file Python CLI utility designed to archive entire project folders (React, Next.js, Python, etc.) into versioned ZIP files with intelligent exclusion rules.

## Features

- **🚀 Quick Archiving**: Zip complex projects with a single command.
- **📅 Smart Versioning**: Automatically generates timestamped filenames (e.g., `my-project_2026-02-10_174500.zip`).
- **🧠 Intelligent Ignoring**: Skips heavy or sensitive directories like `node_modules`, `.git`, `.next`, and `venv` by default.
- **🛠️ Fully Customizable**: Add your own ignore patterns for directories, files, or extensions via CLI flags.
- **🛡️ Safe Path Handling**: Validates source directories and ensures output paths exist.
- **📊 Detailed Logging**: Clean console output showing exactly what is being added and what is being skipped.

## Installation

Project Zipper is a standalone Python script. No installation is required other than having Python 3.6+ installed on your system.

1. Download `project_zipper.py`.
2. Move it to your project root or add it to your System PATH.

## Usage

### Basic Usage
Zip the current directory to a timestamped file in the same folder:
```bash
python project_zipper.py .
```

### Specify Output Path
Save the zip to a specific location:
```bash
python project_zipper.py /path/to/source -o /backups/my_project.zip
```

### Advanced Filtering
Exclude additional directories and files:
```bash
python project_zipper.py . --ignore-dirs "temp,logs" --ignore-files "secrets.json" --ignore-exts ".bak,.old"
```

## Default Exclusions
By default, Project Zipper ignores:
- **Directories**: `node_modules`, `.git`, `.next`, `.turbo`, `dist`, `build`, `__pycache__`, `venv`, etc.
- **Files**: `.DS_Store`, `Thumbs.db`
- **Extensions**: `.log`, `.tmp`, `.swp`

## Technical Details
- **Language**: Python 3.6+
- **Standard Libraries**: `zipfile`, `pathlib`, `argparse`, `os`, `sys`, `datetime`
- **Compression**: ZIP_DEFLATED (High efficiency)

---
Built with passion by **KaneSoftLab**. Engineering Wisdom for all.
