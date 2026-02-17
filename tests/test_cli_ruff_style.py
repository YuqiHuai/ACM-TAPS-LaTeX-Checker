import subprocess
import sys


def test_cli_outputs_line_numbers(tmp_path):
    tex = tmp_path / "bad.tex"
    tex.write_text(
        r"""
        \\usepackage{amsmath}
        \\usepackage{badpkg}
        """
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "acm_taps_latex_check.cli",
            str(tex),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert ":3:" in result.stdout  # line number check
    assert "badpkg" in result.stdout
