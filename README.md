# File Integrity Monitor

A Python-based file integrity monitoring tool that uses **SHA-256** hashes to detect added, modified, and deleted files.

## Why I built this

This project was built to move beyond theory and practice a core security concept: **file integrity monitoring**.

Instead of only checking whether a file exists, the tool creates a cryptographic fingerprint for every monitored file and compares those fingerprints during later scans.

## Features

- SHA-256 file hashing
- Recursive directory scanning
- JSON baseline creation
- Added file detection
- Modified file detection
- Deleted file detection
- Unchanged file reporting
- Command-line interface
- Automated unit tests
- GitHub Actions CI
- Standard-library-only implementation

## Architecture

```text
                 ┌──────────────────┐
                 │  Monitored Files │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   SHA-256 Hash   │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      ┌──────────────┐          ┌──────────────┐
      │   Baseline   │          │ Current Scan │
      │     JSON     │          │    Hashes    │
      └──────┬───────┘          └──────┬───────┘
             │                         │
             └────────────┬────────────┘
                          ▼
                 ┌──────────────────┐
                 │    Comparison    │
                 └────────┬─────────┘
                          ▼
             Added / Modified / Deleted
```

## Requirements

- Python 3.10+
- No third-party packages

## Quick Start

Clone the repository:

```bash
git clone https://github.com/btwsalts/file-integrity-monitor.git
cd file-integrity-monitor
```

Create a test directory:

```bash
mkdir -p monitored
echo "important data" > monitored/example.txt
```

Create a baseline:

```bash
python3 src/fim.py baseline monitored
```

Scan the directory later:

```bash
python3 src/fim.py scan monitored
```

If a file changes:

```bash
echo "changed data" > monitored/example.txt
python3 src/fim.py scan monitored
```

Example output:

```text
FILE INTEGRITY SCAN
────────────────────────────────
[!] MODIFIED  example.txt

────────────────────────────────
Files scanned: 1
Unchanged:     0
Modified:      1
Added:         0
Deleted:       0
```

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

GitHub Actions also runs the test suite automatically on pushes and pull requests.

## Project Structure

```text
file-integrity-monitor/
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   └── fim.py
├── tests/
│   └── test_fim.py
├── .gitignore
├── PROJECT_OVERVIEW.md
├── README.md
└── requirements.txt
```

## Security Considerations

SHA-256 provides a strong cryptographic fingerprint for detecting file-content changes, but the baseline must be treated as trusted data.

For stronger real-world protection, a production system could use a digitally signed or externally protected baseline and send scan results to a separate logging system.

## What I Learned

Building this project gave me hands-on practice with:

- Cryptographic hashing
- Python file handling
- Recursive filesystem traversal
- CLI design
- Baseline comparison logic
- Automated testing
- Continuous integration
- Security limitations and threat modeling

## Roadmap

- [ ] Signed baselines
- [ ] Webhook/email alerts
- [ ] Scheduled scans
- [ ] JSON scan reports
- [ ] Configurable include/exclude rules
- [ ] Optional encrypted baseline
- [ ] Packaging for easier installation

## Disclaimer

This project is intended for learning, experimentation, and local file monitoring. It is not a replacement for a dedicated enterprise file integrity monitoring or endpoint security platform.
