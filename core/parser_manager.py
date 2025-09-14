from typing import Dict, Any, Callable
from parsers import json as json_parser
from parsers import nginx as nginx_parser
from parsers import apache as apache_parser
from parsers import syslog as syslog_parser
from parsers import postgres as postgres_parser
from parsers import generic as generic_parser
from core.logger import log

# Registry of available parsers
PARSER_REGISTRY: Dict[str, Callable[[str], Dict[str, Any]]] = {
    "json": json_parser.parse,
    "nginx": nginx_parser.parse,
    "apache": apache_parser.parse,
    "syslog": syslog_parser.parse,
    "postgres": postgres_parser.parse,
    "generic": generic_parser.parse,
}


class ParserManager:
    def __init__(self):
        self.parsers = PARSER_REGISTRY.copy()

    def register_parser(self, name: str, parser_func: Callable[[str], Dict[str, Any]]):
        if name in self.parsers:
            log(f"Parser {name} already exists. Overwriting.", level="WARNING")
        self.parsers[name] = parser_func
        log(f"Registered parser: {name}")

    def unregister_parser(self, name: str):
        if name in self.parsers:
            del self.parsers[name]
            log(f"Unregistered parser: {name}")
        else:
            log(f"Parser {name} not found.", level="WARNING")

    def parse(self, log_type: str, line: str) -> Dict[str, Any]:
        parser = self.parsers.get(log_type)
        if not parser:
            log(f"No parser found for type '{log_type}', using generic parser.", level="WARNING")
            parser = generic_parser.parse

        try:
            parsed = parser(line)
            return parsed
        except Exception as e:
            log(f"Parsing failed for line '{line}': {e}", level="ERROR")
            return {}

    def list_parsers(self) -> list:
        return list(self.parsers.keys())
