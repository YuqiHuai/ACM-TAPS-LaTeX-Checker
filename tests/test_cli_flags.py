import subprocess
import sys


def test_cli_json_output(tmp_path):
    tex = tmp_path / "bad.tex"
    tex.write_text(r"\usepackage{unknownpkg}")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_checker.cli",
            str(tex),
            "--json",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "unknownpkg" in result.stdout
    assert "{" in result.stdout  # basic JSON sanity check


def test_cli_recursive(tmp_path):
    subdir = tmp_path / "sub"
    subdir.mkdir()

    tex = subdir / "bad.tex"
    tex.write_text(r"\usepackage{unknownpkg}")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_checker.cli",
            str(tmp_path),  # no --recursive
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "unknownpkg" in result.stdout
