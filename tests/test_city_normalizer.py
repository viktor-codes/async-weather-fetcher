from app.services.city_normalizer import normalize_city


def test_normalize_city_misspelling():
    # Minor typo in the name
    assert normalize_city("Londn") == "London"


def test_normalize_city_cyrillic():
    # Cyrillic should transliterate and match via fuzzy matching
    assert normalize_city("Киев") == "Kyiv"


def test_normalize_city_unknown_returns_clean_transliteration():
    # Unknown cities get cleaned transliteration as the output
    assert normalize_city("Xyzqwerty") == "Xyzqwerty"

