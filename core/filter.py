import re
from typing import Dict, Any, List
from core.logger import log

# Each rule can include field, regex, value conditions, etc.
DEFAULT_FILTER_RULES: List[Dict[str, Any]] = [
    # Example: {"field": "level", "equals": "ERROR"}
    # Example: {"field": "message", "regex": "timeout|failed"}
]


def apply_filter(record: Dict[str, Any], rules: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    if rules is None:
        rules = DEFAULT_FILTER_RULES

    for rule in rules:
        field = rule.get("field")
        if field not in record:
            continue

        # Exact value match
        if "equals" in rule and record[field] != rule["equals"]:
            return None

        # Value in list
        if "in" in rule and record[field] not in rule["in"]:
            return None

        # Regex match
        if "regex" in rule:
            if not re.search(rule["regex"], str(record[field])):
                return None

        # Greater/Less than for numeric fields
        if "gt" in rule:
            try:
                if float(record[field]) <= float(rule["gt"]):
                    return None
            except ValueError:
                return None
        if "lt" in rule:
            try:
                if float(record[field]) >= float(rule["lt"]):
                    return None
            except ValueError:
                return None

    return record


def add_rule(field: str, equals=None, regex=None, in_list=None, gt=None, lt=None, rules: List[Dict] = None):
    """
    Helper to add a new filter rule dynamically.
    """
    rule = {"field": field}
    if equals is not None:
        rule["equals"] = equals
    if regex is not None:
        rule["regex"] = regex
    if in_list is not None:
        rule["in"] = in_list
    if gt is not None:
        rule["gt"] = gt
    if lt is not None:
        rule["lt"] = lt

    if rules is not None:
        rules.append(rule)
    else:
        DEFAULT_FILTER_RULES.append(rule)
    log(f"Added new filter rule: {rule}")


def clear_rules(rules: List[Dict] = None):
    """
    Clear all filter rules.
    """
    if rules is not None:
        rules.clear()
    else:
        DEFAULT_FILTER_RULES.clear()
    log("Cleared all filter rules")
