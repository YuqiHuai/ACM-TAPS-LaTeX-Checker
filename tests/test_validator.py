from acm_taps_latex_check.validator import find_unsupported_packages


def test_no_unsupported_packages():
    used = {"amsmath", "graphicx"}
    supported = ["amsmath", "graphicx", "hyperref"]

    unsupported = find_unsupported_packages(used, supported)

    assert (
        unsupported == set()
    ), f"Expected no unsupported packages, but got {unsupported}"


def test_detect_unsupported_packages():
    used = {"amsmath", "unknownpkg"}
    supported = ["amsmath", "graphicx"]

    unsupported = find_unsupported_packages(used, supported)

    assert unsupported == {
        "unknownpkg"
    }, f"Expected {{'unknownpkg'}}, but got {unsupported}"
