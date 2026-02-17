from importlib import resources
from typing import List


def load_additional_packages() -> List[str]:
    """
    Load packages that are implicitly included by the ACM class file.
    """
    with (
        resources.files("acm_taps_packages.data")
        .joinpath("additional.txt")
        .open("r", encoding="utf-8") as f
    ):
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]
