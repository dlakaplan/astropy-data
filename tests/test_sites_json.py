import json
import os


def test_sites():
    """Test the file is loadable, does not vet the content."""
    filename = os.path.join(
        os.path.dirname(__file__), os.pardir, "coordinates", "sites.json"
    )
    with open(filename) as fin:
        data = json.load(fin)

    # Basic check on the default site
    assert "greenwich" in data and data["greenwich"]["timezone"] == "Greenwich"


def test_sites_duplicates():
    filename = os.path.join(
        os.path.dirname(__file__), os.pardir, "coordinates", "sites.json"
    )
    with open(filename) as fin:
        data = json.load(fin)
    # get a dictionary where the keys are the primary names and the data are the aliases
    # primary names are already required to be unique, so this will not have collisions
    all_names = {x: set([x] + data[x]["aliases"]) for x in data}
    # then find all names/aliases that were used
    # only insert after checking for duplication so we don't overwrite previous entries
    # the keys will be all of the aliases, and the values will be the primary names
    used_names = {}
    for k, v in all_names.items():
        for n in v:
            if n not in used_names:
                used_names[n] = k
            else:
                raise ValueError(
                    f"Facility '{n}' (primary name '{k}') is already present (primary name '{used_names[n]}')"
                )
