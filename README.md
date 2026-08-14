# Douala Ride AI

AI-powered urban mobility platform designed for Douala, Cameroon.

## Vision

**Tell the AI where you need to go. Let the AI handle the journey.**

Douala Ride is designed as an AI mobility operating system rather than a conventional ride-hailing clone.

## Architecture

- Python + Flask API
- MySQL + SQLAlchemy
- Mistral AI agent with controlled backend tools
- OpenStreetMap + Leaflet + OSRM routing
- Mobile Money through PawaPay or compatible provider
- Real-time driver/trip tracking
- Passenger application
- Driver application
- Mobility Command Center for administrators

## Core rule

The AI never directly accesses the database. Every action follows:

`AI -> Tool -> Backend Service -> Validation -> Database / External API`

## Primary demo

> I need to go from Bonaberi to Akwa before 8 AM and I have a budget of 1,500 FCFA.

The platform should plan the journey, compare transport options, match a driver, book, initiate payment, track the journey and expose the trip to the administrator dashboard.

## Development

See `.env.example` for configuration. Start with the backend foundation, then build the end-to-end Bonaberi-to-Akwa journey before expanding the feature set.
