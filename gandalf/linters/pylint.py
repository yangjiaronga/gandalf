import re

from gandalf.problem import Problem

from typing import Set

PYLINT_LINE_REGEX = re.compile(r'(?P<path>[^:]*):(?P<line>\d*):\s*'
                               r'(?:(?P<column>\d*):)?\s*'
                               r'(?P<message>.*)')


def parse(contents: str) -> Set[Problem]:
    result = set()  # type: Set[Problem]
    for line in contents.splitlines():
        match = PYLINT_LINE_REGEX.match(line)
        if match:
            groups = match.groupdict()
            path = groups['path']
            if path.startswith('./'):
                path = path[2:]
            result.add(Problem(path, groups['line'], groups['message']))
    return result
