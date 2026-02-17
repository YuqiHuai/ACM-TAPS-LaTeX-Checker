import subprocess
import sys

from acm_taps_latex_check.load_additional import load_additional_packages
from acm_taps_latex_check.load_local_list import load_local_list


def get_supported_non_duplicate_package():
    supported = set(load_local_list())
    additional = set(load_additional_packages())

    # choose one supported package that is NOT auto-loaded
    candidates = supported - additional

    if not candidates:
        raise RuntimeError("No supported non-duplicate packages available for testing.")

    return sorted(candidates)[0]


def test_cli_detects_unsupported_package(tmp_path):
    tex_file = tmp_path / "bad.tex"
    tex_file.write_text(
        r"""
        \usepackage{thispackagedoesnotexist}
        """
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_check.cli",
            str(tex_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "TAPS001" in result.stdout
    assert "thispackagedoesnotexist" in result.stdout


def test_cli_detects_duplicate_package(tmp_path):
    from acm_taps_latex_check.load_additional import load_additional_packages
    from acm_taps_latex_check.load_local_list import load_local_list

    supported = set(load_local_list())
    additional = set(load_additional_packages())

    # Only duplicates if package is both supported and additional
    candidates = supported & additional

    if not candidates:
        # Nothing valid to test
        return

    duplicate_pkg = sorted(candidates)[0]

    tex_file = tmp_path / "dup.tex"
    tex_file.write_text(
        rf"""
        \usepackage{{{duplicate_pkg}}}
        """
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_check.cli",
            str(tex_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "TAPS002" in result.stdout
    assert duplicate_pkg in result.stdout


def test_cli_accepts_supported_packages(tmp_path):
    safe_pkg = get_supported_non_duplicate_package()

    tex_file = tmp_path / "valid.tex"
    tex_file.write_text(
        rf"""
        \usepackage{{{safe_pkg}}}
        """
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_check.cli",
            str(tex_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"Expected exit code 0 for valid packages, " f"but got {result.returncode}"
    )

    assert "All packages supported." in result.stdout
