# Douala Ride AI — Presentation Guide

## 1. Opening — 30 seconds

**Problem:** Douala mobility is fragmented by fare negotiation, uncertain routes, limited accountability and safety concerns.

**Our idea:** We are not building another app where the passenger fills forms and searches through options. We are building an AI mobility operating system where the passenger describes the transportation objective in natural language and the system coordinates the journey.

Say:

> "Instead of asking the passenger to operate the transport system, we let the passenger describe the goal and let the Mobility Agent coordinate the journey."

## 2. Primary demonstration

Say:

> "I need to go from Bonaberi to Akwa before 8 AM and I have a budget of 1,500 FCFA."

Show the sequence:

`Passenger -> Mistral -> location tools -> route/fare engine -> driver matching -> recommendation -> confirmation -> booking -> PawaPay -> callback -> trip`

## 3. What makes the AI real

Do not describe it as a chatbot.

The Mistral model receives controlled function definitions. It can request approved functions such as location search, trip planning, driver discovery and booking. The backend validates every call before touching the database or an external service.

Key sentence:

> "The model decides what tool is needed; the backend decides whether that action is valid."

## 4. Universal location architecture

Explain that Bonaberi -> Akwa is only the demonstration route.

The backend accepts any pickup and destination coordinates, so the route is calculated dynamically rather than hard-coded for a list of routes.

`Any pickup + Any destination -> OSRM -> distance + ETA -> fare -> driver matching`

## 5. Driver matching

The matching layer uses actual platform data:

- online status
- driver verification
- safety status
- active verified vehicle
- vehicle type
- current location
- distance from pickup
- rating

The AI does not invent a driver.

## 6. Payment

Explain:

`Booking -> PawaPay deposit -> Mobile Money authorization -> asynchronous callback -> payment status persistence`

Payment status is controlled by the backend. The frontend cannot declare a successful payment.

For the presentation, use the PawaPay sandbox. Cameroon supports MTN and Orange providers through `MTN_MOMO_CMR` and `ORANGE_CMR`.

## 7. Why this is different from Uber/Yango/Gozem

Do not claim that those platforms are technically incapable of AI. Instead explain the product experience difference:

Traditional flow:

`Open app -> choose fields -> select vehicle -> book`

Douala Ride flow:

`Express objective -> AI understands constraints -> AI gathers mobility data -> AI recommends -> passenger confirms -> system executes`

The differentiation is the **AI-first interaction model plus Douala-specific operational intelligence**.

## 8. Architecture answer if the teacher asks

`Passenger App`

`-> Flask REST API`

`-> Mobility Agent`

`-> Allow-listed tools`

`-> Services`

`-> MySQL / OSRM / PawaPay`

The AI never accesses MySQL directly.

## 9. Security answer

Mention:

- secrets stay in environment variables
- no API keys in GitHub
- allow-listed AI tools
- backend validation
- controlled trip state machine
- payment callback is authoritative
- driver verification and safety filters

## 10. If asked about limitations

Be honest:

> "This is a technically credible prototype. Production deployment would still require hardened authentication/authorization, signed payment callback verification, production monitoring, scalable real-time location infrastructure, provider configuration and full mobile application deployment."

This answer demonstrates engineering maturity.

## 11. Closing

> "Our goal is not to make another ride-hailing interface. Our goal is to make transportation in Douala something people can simply ask for. Tell the AI where you need to go, explain your constraints, and let the system coordinate the journey."
