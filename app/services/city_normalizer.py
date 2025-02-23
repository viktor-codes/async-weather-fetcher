import json
import re
from fuzzywuzzy import process, fuzz
from unidecode import unidecode
import os


def load_city_list(json_file=None):
    """
    Loads a list of known cities from a JSON file.
    The file should contain a JSON array of strings.
    """
    if json_file is None:
        json_file = os.path.join(os.path.dirname(__file__), "city_list.json")

    with open(json_file, "r", encoding="utf-8") as f:
        cities = json.load(f)
    return cities


# Load the known city names in English
KNOWN_CITIES_EN = load_city_list()


def normalize_city(city_input: str, threshold: int = 55) -> str:
    """
    Accepts a city name input (with typos or in different languages),
    cleans it using regular expressions, transliterates it into Latin,
    converts it to lowercase, and returns the correct city name in English
    if a sufficiently similar match is found. Otherwise, returns
    the cleaned version.
    """
    # 1. Cleaning: Keep only letters and spaces
    cleaned = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", city_input)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # 2. Transliteration: Convert Cyrillic and other symbols to Latin
    transliterated = unidecode(cleaned)

    # 3. Convert to lowercase for comparison
    normalized_input = transliterated.lower()

    # 4. Create a dictionary mapping
    cities_map = {city.lower(): city for city in KNOWN_CITIES_EN}

    # 5. Use fuzzy matching to find the best match
    best_match = process.extractOne(
        normalized_input, list(cities_map.keys()), scorer=fuzz.ratio
    )
    if best_match and best_match[1] >= threshold:
        return cities_map[best_match[0]]

    return transliterated
