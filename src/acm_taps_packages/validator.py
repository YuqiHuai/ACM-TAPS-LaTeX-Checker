from pathlib import Path
from typing import Dict, List, Set

from acm_taps_latex_checker.latex_parser import extract_packages_with_lines
from acm_taps_latex_checker.load_additional import load_additional_packages
from acm_taps_latex_checker.load_local_list import load_local_list

# -------------------------------------------------
# Error Codes
# -------------------------------------------------

UNSUPPORTED_CODE = "TAPS001"
DUPLICATE_CODE = "TAPS002"


# -------------------------------------------------
# Simple set-based validation (backward compatible)
# -------------------------------------------------


def find_unsupported_packages(
    used_packages: Set[str],
    supported_packages: List[str],
) -> Set[str]:
    return used_packages - set(supported_packages)


def validate_tex_file(path: Path) -> Set[str]:
    content = path.read_text(encoding="utf-8")

    used_with_lines = extract_packages_with_lines(content)
    used_packages = set(used_with_lines.keys())
    supported = load_local_list()

    return find_unsupported_packages(used_packages, supported)


# -------------------------------------------------
# Structured validation with line numbers
# -------------------------------------------------


def validate_tex_file_with_lines(
    path: Path,
) -> Dict[str, Dict[str, List[int]]]:
    """
    Returns:
        {
            "unsupported": { pkg: [lines] },
            "duplicate": { pkg: [lines] }
        }
    """
    content = path.read_text(encoding="utf-8")

    used = extract_packages_with_lines(content)
    supported = set(load_local_list())
    additional = set(load_additional_packages())

    unsupported = {}
    duplicate = {}

    for pkg, lines in used.items():
        if pkg not in supported:
            unsupported[pkg] = lines
        elif pkg in additional:
            duplicate[pkg] = lines

    return {
        "unsupported": unsupported,
        "duplicate": duplicate,
    }


# -------------------------------------------------
# Directory validation
# -------------------------------------------------


def validate_directory(
    path: Path,
) -> Dict[Path, Dict[str, Dict[str, List[int]]]]:
    results = {}

    for tex_file in path.rglob("*.tex"):
        errors = validate_tex_file_with_lines(tex_file)

        if errors["unsupported"] or errors["duplicate"]:
            results[tex_file] = errors

    return results
