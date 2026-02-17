import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.text import Text

from acm_taps_packages.validator import (
    DUPLICATE_CODE,
    UNSUPPORTED_CODE,
    validate_directory,
    validate_tex_file_with_lines,
)

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taps-latex-check",
        description="Validate LaTeX files against ACM TAPS supported packages.",
    )

    parser.add_argument("path", help="Path to .tex file or directory")

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    return parser


def format_error_line(
    path: Path,
    lineno: int,
    code: str,
    message: str,
) -> Text:
    """
    Create colored ruff-style error line.
    """

    line = Text()

    line.append(str(path), style="bold")
    line.append(f":{lineno}: ", style="dim")

    line.append(f"{code} ", style="bold red")
    line.append(message, style="red")

    return line


def print_errors_sorted(path: Path, errors: Dict[str, Dict[str, List[int]]]):
    """
    Print errors sorted deterministically.
    """

    items = []

    # Collect all errors first
    for pkg, lines in errors["unsupported"].items():
        for lineno in lines:
            items.append((lineno, pkg, UNSUPPORTED_CODE, "Unsupported module"))

    for pkg, lines in errors["duplicate"].items():
        for lineno in lines:
            items.append(
                (
                    lineno,
                    pkg,
                    DUPLICATE_CODE,
                    "Duplicate module (already loaded by ACM class)",
                )
            )

    # Sort deterministically
    items.sort(key=lambda x: (x[0], x[1], x[2]))

    # Print
    for lineno, pkg, code, msg in items:
        text = format_error_line(
            path,
            lineno,
            code,
            f"{msg} ['{pkg}']",
        )
        console.print(text)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        console.print(f"[red]Error: Path not found: {path}[/red]")
        sys.exit(1)

    # FILE MODE
    if path.is_file():
        errors = validate_tex_file_with_lines(path)

        has_errors = bool(errors["unsupported"] or errors["duplicate"])

        if args.json:
            print(json.dumps(errors, indent=2))
        else:
            if has_errors:
                print_errors_sorted(path, errors)
            else:
                console.print("[green]All packages supported.[/green]")

        sys.exit(1 if has_errors else 0)

    # DIRECTORY MODE
    if path.is_dir():
        results = validate_directory(path)

        has_errors = bool(results)

        if args.json:
            print(
                json.dumps(
                    {str(p): e for p, e in results.items()},
                    indent=2,
                )
            )
        else:
            # Sort files deterministically
            for file_path in sorted(results.keys()):
                print_errors_sorted(file_path, results[file_path])

            if not has_errors:
                console.print("[green]All packages supported.[/green]")

        sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
