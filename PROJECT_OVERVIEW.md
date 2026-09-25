# Project Overview

## File Integrity Monitor

File Integrity Monitor (FIM) is a Python command-line security project that detects changes to files by comparing their current SHA-256 hashes against a trusted baseline.

### Purpose

The project demonstrates practical security concepts:

- Cryptographic hashing
- File integrity monitoring
- Baseline creation
- Change detection
- Command-line tooling
- Automated testing
- Continuous integration

### How it works

1. The user selects a directory to monitor.
2. FIM recursively reads its files.
3. Each file is hashed with SHA-256.
4. The hashes are stored in a JSON baseline.
5. A later scan creates a fresh set of hashes.
6. FIM compares the two sets and reports:
   - Added files
   - Modified files
   - Deleted files
   - Unchanged files

### Main components

- `pathlib` — filesystem traversal and paths
- `hashlib` — SHA-256 hashing
- `json` — baseline storage
- `argparse` — CLI interface
- `unittest` — automated tests

### Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Scan completed with no detected changes |
| 1 | Scan completed and changes were detected |
| 2 | Invalid input or runtime error |

### Threat model

The tool is designed to detect accidental or unauthorized file changes when the baseline is trusted.

The baseline itself must be protected. If an attacker can modify both the monitored files and the baseline, this local tool cannot independently establish which state is trustworthy.

### Limitations

This is an educational/local monitoring tool. It does not provide:

- Remote alerting
- A tamper-proof baseline
- Authentication
- Centralized logging
- Enterprise endpoint management
- Malware attribution

### Future improvements

- HMAC or digitally signed baselines
- Email/webhook alerts
- Scheduled monitoring
- Structured JSON scan reports
- Configuration files
- Ignore/include rules
- Cross-platform packaging
- Optional encrypted baseline storage
