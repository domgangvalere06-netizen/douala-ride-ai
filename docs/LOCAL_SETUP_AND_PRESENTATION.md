# Douala Ride AI — Local Setup & Presentation Runbook

## 1. Clone the repository

```bash
git clone https://github.com/domgangvalere06-netizen/douala-ride-ai.git
cd douala-ride-ai
git checkout architecture-rebuild
```

## 2. Create the Python environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Create the local environment file

Copy `.env.example` to `.env` and fill in the real secrets locally.

Never commit `.env` to GitHub. The repository `.gitignore` already excludes it.

Required secrets:

```env
MISTRAL_API_KEY=your_real_key
PAWAPAY_API_TOKEN=your_sandbox_token
PAWAPAY_CALLBACK_URL=https://your-public-url/api/payments/webhook
```

Use PawaPay sandbox for the presentation. Do not use a live payment token for development.

## 4. Database

Create a MySQL database named `douala_ride`, then set `DATABASE_URL` in `.env`.

Example:

```env
DATABASE_URL=mysql+pymysql://douala_ride:password@localhost:3306/douala_ride
```

Run the repository's migration/schema commands if present before starting the server.

## 5. Start Flask

Use the repository's existing entry point. If `run.py` is present:

```bash
python run.py
```

Otherwise use Flask's application factory:

```bash
flask --app app:create_app run --debug
```

## 6. Presentation smoke test

The most important scenario is:

> I need to go from Bonaberi to Akwa before 8 AM and I have a budget of 1,500 FCFA.

Expected architecture:

Passenger → Mistral → location search → universal trip planner → OSRM route → fare engine → driver matching → passenger confirmation → booking → PawaPay → webhook/status confirmation → driver/trip tracking.

## 7. What to verify before presenting

- [ ] Mistral API key loads from environment variables.
- [ ] Mistral can call only registered/allowed tools.
- [ ] Arbitrary pickup/destination coordinates can be planned.
- [ ] OSRM returns route distance and ETA.
- [ ] Fare engine returns moto and car estimates.
- [ ] Driver matching uses real database records, not hard-coded demo drivers.
- [ ] Booking requires passenger confirmation.
- [ ] PawaPay uses sandbox and asynchronous payment confirmation.
- [ ] Webhook is reachable from the public internet.
- [ ] Payment status is verified server-side.
- [ ] Trip state transitions are enforced server-side.
- [ ] Admin dashboard can show real trip/payment data.
- [ ] `.env` is not committed.

## 8. Presentation narrative

### Problem
Douala mobility is affected by fare negotiation, uncertain routes, fragmented transport choices, safety concerns and limited accountability.

### Innovation
Douala Ride is an AI mobility platform. The passenger describes the transportation objective in natural language and the Mobility Agent coordinates the journey through controlled backend tools.

### Demonstration
1. Passenger gives a natural-language request.
2. AI identifies pickup, destination, budget and constraints.
3. Map service resolves locations and calculates a road route.
4. Fare engine compares moto and car.
5. Driver service finds verified nearby drivers.
6. AI recommends the best available option.
7. Passenger confirms.
8. Booking is created.
9. PawaPay handles Mobile Money initiation.
10. Server receives and verifies asynchronous payment status.
11. Driver accepts and trip begins.
12. Passenger sees live trip status.
13. Admin sees the operational event on the command center.

### Key message
"We are not building another Uber, Yango or Gozem clone. We are changing the interaction model: the passenger describes the mobility objective, and the AI coordinates the journey through controlled services."
