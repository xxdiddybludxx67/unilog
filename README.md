# Unilog-Py

A **Work-in-Progress (WIP) Python log processing framework**.  
Unilog-Py provides tools to **ingest, parse, tail, and output logs** from multiple sources, with modular support for:

- **Parsers**: Apache, Nginx, Syslog, JSON logs
- **ML modules**: anomaly detection and clustering
- **Outputs**: CSV, JSON, Elastic (planned)
- **Cloud support**: S3, GCP, Azure (stubs for now)
- **Database support**: SQLite, PostgreSQL (stubs for now)
- **CLI utilities**: ingest, parse, tail logs
- **VSCode extension**: optional support for viewing logs in editor

> **Currently in development. Modules are functional but not finalised.**

---

## Features

- Read and tail log files
- Auto-detect log formats
- Parse multiple log types
- Output parsed logs to CSV/JSON
- ML anomaly detection and clustering
- Minimal cloud and DB integration stubs
- Modular, scalable architecture

---

## Folder Structure

unilog-py/
├── src/
│ ├── cli/
│ ├── core/
│ ├── parsers/
│ ├── outputs/
│ ├── cloud/
│ ├── dashboard/
│ ├── vscode_ext/
│ └── db/
├── tests/
├── README.md
├── .gitignore
└── requirements.txt


---

## Dependencies

- Python 3.10+  
- Standard Python libraries (built-in):
  - `json`
  - `csv`
  - `unittest`
  - `os`
  - `pathlib`
- Optional (for future ML modules):
  - `numpy`
  - `scikit-learn`  

You can install optional dependencies with:

/bash
pip install numpy scikit-learn

Getting Started

    Clone the repository:

git clone https://github.com/YOUR_USERNAME/unilog-py.git
cd unilog-py

    Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

    Install dependencies:

pip install -r requirements.txt

    Currently most modules use only standard library, so requirements.txt may be empty.

    Run tests:

python -m unittest discover -s tests -p "test*.py" -v

    This will run all test cases in tests/.

    Example usage:

from src.cli.ingest import Ingest
lines = Ingest.read_file("tests/sample.log")
print(lines[:5])

Development Notes

    All modules are WIP; interfaces may change frequently.

    You can contribute parsers, outputs, and ML modules.

    Use tests/ for writing unit tests for new functionality. (Tests are gpt'd might be poor quality)
