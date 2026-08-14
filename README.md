# Douala Ride AI

**AI-powered urban mobility platform designed specifically for Douala, Cameroon.**

> **Tell the AI where you need to go. Let the AI handle the journey.**

Douala Ride is designed as an **AI mobility operating system**, not another conventional ride-hailing clone.

## Architecture

- Python + Flask REST API
- MySQL + SQLAlchemy + migrations
- Mistral AI Mobility Agent with controlled function calling
- OpenStreetMap + Nominatim + Leaflet + OSRM routing
- Database-backed driver matching
- PawaPay Mobile Money integration for Cameroon
- Passenger, driver and administrator experiences
- Safety, ratings, trip sharing and operational analytics

## AI safety boundary

The AI never receives database credentials and never executes SQL directly:

`AI -> Allow-listed Tool -> Backend Service -> Validation -> Database / External API`

## Universal trip planning

Trip planning is location-independent. The same engine accepts any supported pickup and destination coordinates:

`Location search -> coordinates -> OSRM route -> distance/ETA -> fare engine -> budget filtering -> driver matching -> recommendation`

## Payment architecture

`Passenger confirmation -> Booking -> Payment record -> PawaPay deposit -> Mobile Money authorization -> Callback -> Payment persistence -> Trip/booking state update`

PawaPay supports MTN and Orange in Cameroon through `MTN_MOMO_CMR` and `ORANGE_CMR`. Sandbox should be used for the presentation before production credentials are introduced.

## Environment

Copy `.env.example` to `.env` and set your own secrets. **Never commit MISTRAL_API_KEY or PAWAPAY_API_TOKEN to GitHub.**

## Presentation demo

Use this natural-language request:

> I need to go from Bonaberi to Akwa before 8 AM and I have a budget of 1,500 FCFA.

Demonstrate:

1. AI understands the mobility objective.
2. Locations are resolved to coordinates.
3. Real road route is calculated.
4. Moto and car fares are calculated by the backend.
5. Budget is considered.
6. Verified/online drivers are matched from the database.
7. AI recommends the best option and explains why.
8. Passenger confirms.
9. Booking is created.
10. PawaPay payment is initiated.
11. PawaPay callback updates payment state.
12. Driver/trip state can continue through the controlled backend.
13. Admin sees the operational data.

See `PRESENTATION.md` for the presentation script and architecture talking points.
