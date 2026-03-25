from app.services.city_normalizer import normalize_city


def test_normalize_city_misspelling():
    # Небольшая ошибка в названии
    assert normalize_city("Londn") == "London"


def test_normalize_city_cyrillic():
    # Кириллица должна транслитерироваться и матчиться fuzzy-механизмом
    assert normalize_city("Киев") == "Kyiv"


def test_normalize_city_unknown_returns_clean_transliteration():
    # Для неизвестных городов функция возвращает очищенную транслитерацию
    assert normalize_city("Xyzqwerty") == "Xyzqwerty"

