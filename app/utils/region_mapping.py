import pycountry
import pycountry_convert as pc
from app.utils.logger import logger


def get_region_for_country(country_name: str) -> str:
    """
    Converts a country name into its corresponding continent.
    Uses `pycountry` and `pycountry-convert` for offline lookup.
    """
    try:
        # Get country code (ISO Alpha-2)
        country = pycountry.countries.lookup(country_name)
        country_code = country.alpha_2

        # Convert to continent code
        continent_code = pc.country_alpha2_to_continent_code(country_code)

        # Map continent code to full continent name
        CONTINENT_MAPPING = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "America",
            "SA": "America",
            "OC": "Oceania",
            "AN": "Antarctica",
        }

        return CONTINENT_MAPPING.get(continent_code, "Unknown")

    except (LookupError, KeyError):
        logger.warning(f"Region not found for country: {country_name}")
        return "Unknown"
