# Douala Ride AI — Demo Checklist

## Before the presentation

1. Create local `.env` from `.env.example`.
2. Set `MISTRAL_API_KEY` locally.
3. Set `PAWAPAY_API_TOKEN` locally.
4. Set `PAWAPAY_API_URL=https://api.sandbox.pawapay.io` for the presentation.
5. Choose `PAWAPAY_PROVIDER=MTN_MOMO_CMR` or `ORANGE_CMR`.
6. Configure `PAWAPAY_CALLBACK_URL` to a publicly reachable HTTPS endpoint pointing to `/api/payments/webhook`.
7. Configure MySQL and run migrations.
8. Seed at least one passenger, one verified online driver, one active verified vehicle and recent driver location.
9. Verify `/health` returns `status=ok`.
10. Verify `/api/ai/tools` includes `plan_trip`, `create_booking`, `initiate_payment` and `get_payment_status`.

## Main live demo

Passenger says:

> I need to go from Bonaberi to Akwa before 8 AM and I have a budget of 1,500 FCFA.

Expected:

- Mistral understands the request.
- Locations are resolved.
- `plan_trip` returns route, distance, duration and fares.
- Driver matching uses real database candidates.
- AI recommends an option.
- Passenger explicitly confirms.
- Booking is created.
- Payment is initiated through PawaPay.
- PawaPay final callback changes payment state.
- Payment status endpoint/AI tool reports the backend status.

## Backup demo

If external provider/network access fails, demonstrate the architecture with a recorded/sandbox response and explain that production payment state is callback-driven. Do not claim that a payment succeeded unless the backend received a successful provider status.

## Security

Never put API keys in GitHub. Keep them in `.env` locally or in deployment secrets. Rotate any key that is accidentally exposed.
