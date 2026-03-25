from app.utils.region_mapping import get_region_for_country


def test_get_region_for_country_known():
    assert get_region_for_country("Ukraine") == "Europe"


def test_get_region_for_country_known_brazil():
    assert get_region_for_country("Brazil") == "America"


def test_get_region_for_country_unknown():
    assert get_region_for_country("Atlantis") == "Unknown"

