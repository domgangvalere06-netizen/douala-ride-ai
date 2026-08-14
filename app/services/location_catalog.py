"""Curated Douala places used for fast, predictable mobility search.

Coordinates are neighborhood/landmark reference points, not house-level
addresses. Unknown or more precise searches should continue to Nominatim.
"""

LOCATIONS = [
    {"name": "Bonaberi", "latitude": 4.0817, "longitude": 9.6492, "type": "neighborhood"},
    {"name": "Akwa", "latitude": 4.0483, "longitude": 9.7043, "type": "neighborhood"},
    {"name": "Bonanjo", "latitude": 4.0435, "longitude": 9.6900, "type": "neighborhood"},
    {"name": "Bonapriso", "latitude": 4.0187, "longitude": 9.6932, "type": "neighborhood"},
    {"name": "Bali", "latitude": 4.0557, "longitude": 9.6940, "type": "neighborhood"},
    {"name": "Deido", "latitude": 4.0616, "longitude": 9.6847, "type": "neighborhood"},
    {"name": "Bépanda", "latitude": 4.0432, "longitude": 9.7288, "type": "neighborhood"},
    {"name": "New Bell", "latitude": 4.0395, "longitude": 9.7150, "type": "neighborhood"},
    {"name": "Nkololoun", "latitude": 4.0390, "longitude": 9.7190, "type": "neighborhood"},
    {"name": "Ndokoti", "latitude": 4.0397, "longitude": 9.7542, "type": "landmark"},
    {"name": "Ndogbong", "latitude": 4.0738, "longitude": 9.7582, "type": "neighborhood"},
    {"name": "Bassa", "latitude": 4.0347, "longitude": 9.7614, "type": "neighborhood"},
    {"name": "Logpom", "latitude": 4.0946, "longitude": 9.7760, "type": "neighborhood"},
    {"name": "Makepe", "latitude": 4.0854, "longitude": 9.7448, "type": "neighborhood"},
    {"name": "Bonamoussadi", "latitude": 4.0875, "longitude": 9.7428, "type": "neighborhood"},
    {"name": "Kotto", "latitude": 4.1050, "longitude": 9.7560, "type": "neighborhood"},
    {"name": "Logbessou", "latitude": 4.1080, "longitude": 9.7820, "type": "neighborhood"},
    {"name": "Yassa", "latitude": 4.0260, "longitude": 9.8190, "type": "neighborhood"},
    {"name": "Japoma", "latitude": 4.0040, "longitude": 9.8060, "type": "neighborhood"},
    {"name": "PK 8", "latitude": 4.0470, "longitude": 9.7850, "type": "area"},
    {"name": "PK 10", "latitude": 4.0410, "longitude": 9.8010, "type": "area"},
    {"name": "PK 12", "latitude": 4.0330, "longitude": 9.8150, "type": "area"},
    {"name": "Bonendale", "latitude": 4.1000, "longitude": 9.6220, "type": "neighborhood"},
    {"name": "Bessengue", "latitude": 4.0650, "longitude": 9.6990, "type": "neighborhood"},
    {"name": "Mabanda", "latitude": 4.0780, "longitude": 9.6660, "type": "neighborhood"},
    {"name": "University of Douala", "latitude": 4.0740, "longitude": 9.7410, "type": "landmark"},
    {"name": "Douala International Airport", "latitude": 4.0060, "longitude": 9.7190, "type": "landmark"},
    {"name": "Port of Douala", "latitude": 4.0400, "longitude": 9.6905, "type": "landmark"},
    {"name": "Douala Grand Mall", "latitude": 4.0180, "longitude": 9.7350, "type": "landmark"},
    {"name": "Marché Central", "latitude": 4.0470, "longitude": 9.7000, "type": "landmark"},
    {"name": "Marché Mboppi", "latitude": 4.0550, "longitude": 9.7120, "type": "landmark"},
    {"name": "Carrefour Ndokoti", "latitude": 4.0397, "longitude": 9.7542, "type": "landmark"},
    {"name": "Rond-point Deido", "latitude": 4.0625, "longitude": 9.6840, "type": "landmark"},
    {"name": "Rond-point Maeturs", "latitude": 4.0750, "longitude": 9.7380, "type": "landmark"},
]


def search(query: str, limit: int = 10):
    q = " ".join(query.lower().strip().split())
    if not q:
        return []
    starts = [x for x in LOCATIONS if x["name"].lower().startswith(q)]
    contains = [x for x in LOCATIONS if q in x["name"].lower() and x not in starts]
    return (starts + contains)[: max(1, min(limit, 50))]
