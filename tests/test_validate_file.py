from acm_taps_latex_checker.validator import validate_tex_file


def test_validate_tex_file(tmp_path):
    tex_file = tmp_path / "test.tex"
    tex_file.write_text(r"\usepackage{amsmath}\n\usepackage{badpkg}")

    unsupported = validate_tex_file(tex_file)

    assert (
        "badpkg" in unsupported
    ), f"Expected 'badpkg' to be unsupported, but got {unsupported}"
