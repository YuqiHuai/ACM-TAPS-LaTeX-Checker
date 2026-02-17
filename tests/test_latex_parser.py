from acm_taps_latex_checker.latex_parser import extract_packages_with_lines


def test_ignore_commented_packages():
    tex = r"""
    % \usepackage{foo}
    \usepackage{bar}
    """

    packages = extract_packages_with_lines(tex)

    assert "foo" not in packages
    assert "bar" in packages
