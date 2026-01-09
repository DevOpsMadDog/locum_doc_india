# LocumMap Chennai (MVP)

Uber-like locum marketplace for Chennai clinics and specialists.

## Architecture
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Realtime**: FastAPI WebSocket rooms per assignment
- **Clinic web**: Next.js (map-first dashboard)
- **Doctor app**: Expo React Native (Android-first)
- **Shared**: Type definitions for shifts/specialties

## Monorepo Structure
```
/apps
  /api             FastAPI backend
  /clinic-web      Next.js dashboard
  /doctor-mobile   Expo doctor app
/packages
  /shared          Shared types
/docs
  openapi.yaml
  postman_collection.json
```

## Local Development
### Backend
```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Clinic Web
```bash
cd apps/clinic-web
npm install
npm run dev
```

### Doctor App (Expo)
```bash
cd apps/doctor-mobile
npm install
npm run start
```

## Docker Compose
```bash
docker-compose up --build
```

## Deployment Guide (Minimal)
1. Provision a PostgreSQL database (Render/Fly.io/Lightsail).
2. Build and deploy `apps/api` container. Set env:
   - `DATABASE_URL`, `JWT_SECRET`, `GOOGLE_MAPS_API_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`
3. Build and deploy `apps/clinic-web` container. Set env:
   - `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
4. Expo doctor app:
   - Configure `EXPO_PUBLIC_API_BASE_URL` in `app.json` or via EAS secrets.

## Chennai Boundary Rule
The MVP enforces a bounding box around Chennai; shift creation outside the boundary is rejected.

## Testing
```bash
pytest apps/api/tests
```
