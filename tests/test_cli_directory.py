import subprocess
import sys


def test_cli_directory_validation(tmp_path):
    # Create valid file
    valid_tex = tmp_path / "valid.tex"
    valid_tex.write_text(
        r"""
        \\usepackage{amsmath}
        \\usepackage{graphicx}
        """
    )

    # Create invalid file
    invalid_tex = tmp_path / "invalid.tex"
    invalid_tex.write_text(
        r"""
        \\usepackage{unknownpkg}
        """
    )

    result = subprocess.run(
        [sys.executable, "-m", "acm_taps_packages.cli", str(tmp_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1, (
        f"Expected exit code 1 for unsupported packages, "
        f"but got {result.returncode}"
    )

    assert "unknownpkg" in result.stdout, (
        f"Expected 'unknownpkg' in output, " f"but got:\n{result.stdout}"
    )
