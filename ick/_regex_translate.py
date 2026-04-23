import re
from typing import Iterable


def rule_name_re(name: str, *, legacy: bool = False) -> str:
    """
    Return a regex used with ``fullmatch`` for rule selection.

    New behavior matches the repo-local rule name exactly.
    Legacy behavior matches the old prefix-aware form, where the prefix and
    rule name were joined with ``/`` and descendants also matched.
    """
    if legacy:
        return f"^{name.replace(':', '/').rstrip('/')}($|/.*$)"
    return f"^{name}$"


def zfilename_re(opts: Iterable[str]) -> re.Pattern[str]:
    o = "|".join(map(re.escape, opts))
    # This regex could be made compatible with `re2` with a minor change of the
    # `(?=\0)` to `\b`.  This will match names like `pyproject.toml.template`
    # by mistake, and we'd need to check the next byte after the end to make
    # sure it's `\0` ourselves.
    s = f"(?:\\A|\\0)(?P<dirname>(?:[^\\0]*/)?)(?P<filename>{o})(?=\0)"
    return re.compile(s)
