# LocumMap Chennai (MVP) Test Plan

## Automated Tests
- **Status machine unit tests**: validates legal shift and assignment transitions.
- **Booking + OTP integration test**: creates clinic + doctor, posts shift, books, and verifies OTP check-in.

Run tests:
```bash
pytest apps/api/tests
```

## Manual QA Checklist
1. Clinic onboarding creates profile within Chennai boundary.
2. Doctor onboarding sets verification status to `pending`.
3. Shift posting outside Chennai is blocked.
4. Doctor accepts shift and status transitions update clinic live view.
5. Location pings accepted only in duty window.
6. OTP check-in requires geofence.
7. Payment order creation + webhook update.
8. Payout placeholder available for admin.
