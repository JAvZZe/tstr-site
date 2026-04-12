"""
List of known testing conglomerate brands for parent/child linking
"""

KNOWN_CONGLOMERATES = [
    "SGS",
    "Intertek",
    "Bureau Veritas",
    "Eurofins",
    "Mistras",
    "Applus",
    "ALS",
    "TUV SUD",
    "TUV Rheinland",
    "TUV Nord",
    "Element Materials Technology",
    "Exova",
    "Baker Hughes",
    "Halliburton",
    "Schlumberger",
    "Weatherford",
    "Dekra",
    "UL Solutions",
    "BSI",
    "Lloyd's Register"
]

def detect_parent(business_name: str):
    """
    Detect if a business name belongs to a known conglomerate.
    Example: 'SGS Houston' -> 'SGS'
    """
    name_upper = business_name.upper()
    for brand in KNOWN_CONGLOMERATES:
        # Check if brand name starts the business name or is a major part of it
        if name_upper.startswith(brand.upper()) or f" {brand.upper()} " in f" {name_upper} ":
            return brand
    return None
