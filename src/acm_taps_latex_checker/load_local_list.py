import json
from importlib import resources


def load_local_list():
    with (
        resources.files("acm_taps_latex_checker.data")
        .joinpath("taps_accepted-packages.json")
        .open("r", encoding="utf-8") as f
    ):
        return json.load(f)
