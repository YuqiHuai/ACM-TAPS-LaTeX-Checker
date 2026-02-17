from acm_taps_packages.load_local_list import load_local_list


def test_load_local_list_returns_list():
    packages = load_local_list()

    assert isinstance(packages, list), (
        f"Expected load_local_list() to return a list, "
        f"but got {type(packages).__name__}"
    )

    assert len(packages) > 0, (
        "Expected package list to be non-empty, " "but it was empty."
    )


def test_load_local_list_correct_length():
    packages = load_local_list()
    expected_length = 147  # exact number from your JSON

    assert len(packages) == expected_length, (
        f"Expected {expected_length} packages, " f"but got {len(packages)}."
    )


def test_load_local_list_contains_expected_packages():
    packages = load_local_list()

    expected_packages = {
        "amsmath",
        "graphicx",
        "hyperref",
        "natbib",
        "xcolor",
    }

    missing = expected_packages - set(packages)

    assert not missing, f"The following expected packages were not found: {missing}"
