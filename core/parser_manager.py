from typing import Dict, Any, Callable
from parsers.json_parser import JSONParser
from parsers.nginx import NginxParser
from parsers.apache import ApacheParser
# from parsers.postgres import PostgresParser  # Uncomment if exists
from parsers.syslog import SyslogParser
from parsers.generic import GenericParser
from core.logger import log

# Registry of available parsers
PARSER_REGISTRY: Dict[str, Callable[[str], Dict[str, Any]]] = {
    "json": JSONParser().parse_line,
    "nginx": NginxParser().parse_line,
    "apache": ApacheParser().parse_line,
    # "postgres": PostgresParser().parse_line,  # Uncomment if exists
    "syslog": SyslogParser().parse_line,
    "generic": GenericParser().parse_line,
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
            from parsers.generic import GenericParser
            parser = GenericParser().parse_line

        try:
            parsed = parser(line)
            return parsed
        except Exception as e:
            log(f"Parsing failed for line '{line}': {e}", level="ERROR")
            return {}

    def list_parsers(self) -> list:
        return list(self.parsers.keys())
