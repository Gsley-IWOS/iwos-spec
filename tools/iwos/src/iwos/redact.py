"""Keep sensitive values out of everything the toolchain prints, writes or returns."""
from __future__ import annotations

import re

MARK = "[redacted]"


def redact(text: str, patterns: list[str]) -> str:
    """Replace every match of a credential pattern. Applied to all output, whatever its source."""
    out = str(text)
    for pattern in patterns:
        try:
            out = re.sub(pattern, MARK, out)
        except re.error:
            continue
    return out


def describe_yaml_error(exc: Exception) -> str:
    """A YAML error without the snippet of the document that the parser quotes."""
    problem = getattr(exc, "problem", None) or "could not be parsed"
    mark = getattr(exc, "problem_mark", None)
    return f"invalid YAML: {problem}" + (f" (line {mark.line + 1})" if mark is not None else "")
