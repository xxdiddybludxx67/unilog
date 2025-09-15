# Unilog-Py

A **Python log processing framework**.  
Unilog-Py provides tools to **ingest, parse, tail, and output logs** from multiple sources, with modular support for:

- **Parsers**: Apache, Nginx, Syslog, JSON logs
- **ML modules**: anomaly detection and clustering
- **Outputs**: CSV, JSON, Elastic (planned)
- **Cloud support**: S3, GCP, Azure (stubs for now)
- **Database support**: SQLite, PostgreSQL (stubs for now)
- **CLI utilities**: ingest, parse, tail logs
- **VSCode extension**: optional support for viewing logs in editor

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
# Core dependencies
- numpy
- scikit-learn
- pandas
- boto3
- google-cloud-storage
- azure-storage-blob
- elasticsearch

# Optional: for web/dashboard features
- dash
- plotly

**You can install all core dependencies with:**
pip install -r requirements.txt

---

## Getting Started

1. Clone the repository:
git clone https://github.com/xxdiddybludxx67/unilog-py.git
cd unilog-py

2. Create a virtual environment :
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate   # macOS/Linux

3. Install dependencies:
pip install -r requirements.txt

4. Run tests:
python -m unittest discover -s tests -p "test_*.py" -v

This will execute all test cases inside the tests/ folder.

5. Example usage:
from cli.ingest import Ingest

lines = Ingest.read_file("tests/sample.log")
print(lines[:5])

Development Notes

    You can contribute parsers, outputs, and ML modules.

    Use tests/ for writing unit tests for new functionality. 
