"""Location search optimized for Douala, with OSM fallback."""

from app.data.douala_locations import DOUALA_LOCATIONS


class LocationService:
    def __init__(self, geocoder=None):
        self.geocoder = geocoder
        self.locations = DOUALA_LOCATIONS

    def search(self, query: str, limit: int = 10):
        query = (query or "").strip().lower()
        if not query:
            return []
        limit = max(1, min(limit, 20))

        exact = []
        partial = []
        for location in self.locations:
            name = location["name"].lower()
            item = {**location, "display_name": f"{location['name']}, Douala, Cameroon", "source": "douala_catalog"}
            if name == query:
                exact.append(item)
            elif query in name:
                partial.append(item)

        results = exact + partial
        if len(results) < limit and self.geocoder:
            try:
                remote = self.geocoder.search(f"{query}, Douala, Cameroon", limit=limit)
                seen = {(round(x["latitude"], 5), round(x["longitude"], 5)) for x in results}
                for item in remote:
                    key = (round(item["latitude"], 5), round(item["longitude"], 5))
                    if key not in seen:
                        results.append({**item, "source": "openstreetmap"})
                        seen.add(key)
            except Exception:
                pass
        return results[:limit]
