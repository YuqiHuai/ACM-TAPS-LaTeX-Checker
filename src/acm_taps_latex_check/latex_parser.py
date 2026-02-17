import re
from typing import Dict, List

USEPACKAGE_PATTERN = re.compile(r"\\usepackage(?:\[[^\]]*\])?{([^}]*)}")


def extract_packages_with_lines(tex_content: str) -> Dict[str, List[int]]:
    """
    Extract package names and their line numbers from LaTeX content.
    Ignores commented lines.
    """

    results: Dict[str, List[int]] = {}

    lines = tex_content.splitlines()

    for lineno, line in enumerate(lines, start=1):
        # Remove comments
        line = line.split("%", 1)[0]

        matches = USEPACKAGE_PATTERN.findall(line)

        for match in matches:
            for pkg in match.split(","):
                pkg = pkg.strip()
                if pkg:
                    results.setdefault(pkg, []).append(lineno)

    return results
