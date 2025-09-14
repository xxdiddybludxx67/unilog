import argparse
from cli.ingest import ingest_logs
from cli.parse import parse_logs
from cli.tail import tail_logs
from cli.utils import helper

def main():
    parser = argparse.ArgumentParser(description="Unilog CLI - Universal log ingestion and parsing")
    parser.add_argument("--ingest", action="store_true", help="Ingest logs")
    parser.add_argument("--parse", action="store_true", help="Parse logs")
    parser.add_argument("--tail", action="store_true", help="Tail logs in real time")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled")

    if args.ingest:
        ingest_logs()
    if args.parse:
        parse_logs()
    if args.tail:
        tail_logs()

if __name__ == "__main__":
    main()
