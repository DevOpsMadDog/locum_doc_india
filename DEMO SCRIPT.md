# LocumMap Chennai (MVP) Demo Script

## Setup
1. Copy `.env.example` to `.env` and add Google Maps + Razorpay keys if available.
2. Start the stack:
   ```bash
   docker-compose up --build
   ```
3. Run migrations:
   ```bash
   docker-compose exec api alembic upgrade head
   ```
4. Seed demo data:
   ```bash
   docker-compose exec api python -m apps.api.scripts.seed
   ```

## Demo Flow
1. **Clinic login**
   - Request OTP: `POST /auth/otp/request`
   - Verify OTP (role `clinic_admin`) to get token.
2. **Create clinic profile**
   - `POST /clinics/me` with Chennai address + lat/lng.
3. **Post a shift**
   - `POST /clinics/shifts` with specialty, time, pay, address.
4. **Match + Book**
   - Use `/clinics/shifts/{id}/book?doctor_id=...` to book a doctor.
5. **Doctor accept + navigate**
   - Doctor OTP login -> `POST /doctors/me`.
   - `POST /doctors/assignments/{id}/accept`.
6. **Live tracking**
   - Doctor app posts `/doctors/assignments/{id}/location` every 10–15s.
   - Clinic subscribes to `ws://localhost:8000/ws/assignments/{id}` for updates.
7. **Check-in/out**
   - Clinic creates OTP: `/assignments/{id}/otp/create?type=checkin`.
   - Doctor verifies: `/assignments/{id}/otp/verify?type=checkin`.
   - Repeat for checkout.
8. **Payments**
   - Create order: `/payments/create-order`.
   - Completion triggers payout: `/payments/payouts/initiate`.
