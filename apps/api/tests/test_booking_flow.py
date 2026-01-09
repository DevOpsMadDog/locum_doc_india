from datetime import datetime, timedelta


def auth_token(client, phone, role):
    resp = client.post("/auth/otp/request", json={"phone": phone})
    otp = resp.json()["dev_otp"]
    verify = client.post(
        "/auth/otp/verify",
        json={"phone": phone, "otp": otp, "role": role},
    )
    return verify.json()["access_token"]


def test_booking_and_otp_flow(client):
    clinic_token = auth_token(client, "+919900000001", "clinic_admin")
    doctor_token = auth_token(client, "+919900000002", "doctor")

    clinic_profile = client.post(
        "/clinics/me",
        headers={"Authorization": f"Bearer {clinic_token}"},
        json={
            "name": "Sunrise Clinic",
            "address": "Nungambakkam, Chennai",
            "lat": 13.06,
            "lng": 80.25,
            "city": "Chennai",
        },
    )
    assert clinic_profile.status_code == 200

    doctor_profile = client.post(
        "/doctors/me",
        headers={"Authorization": f"Bearer {doctor_token}"},
        json={
            "full_name": "Dr. Anya Rao",
            "specialty": "dentist_general",
            "reg_no": "TN12345",
        },
    )
    assert doctor_profile.status_code == 200
    doctor_id = doctor_profile.json()["id"]

    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=4)
    shift = client.post(
        "/clinics/shifts",
        headers={"Authorization": f"Bearer {clinic_token}"},
        json={
            "specialty": "dentist_general",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "pay_amount": 4500,
            "address": "T Nagar, Chennai",
            "lat": 13.04,
            "lng": 80.23,
            "notes": "Bring toolkit",
            "auto_replace": True,
        },
    )
    assert shift.status_code == 200
    shift_id = shift.json()["id"]

    assignment = client.post(
        f"/clinics/shifts/{shift_id}/book",
        headers={"Authorization": f"Bearer {clinic_token}"},
        params={"doctor_id": doctor_id},
    )
    assert assignment.status_code == 200
    assignment_id = assignment.json()["assignment_id"]

    otp_resp = client.post(
        f"/assignments/{assignment_id}/otp/create",
        headers={"Authorization": f"Bearer {clinic_token}"},
        params={"type": "checkin"},
    )
    otp = otp_resp.json()["otp"]

    verify = client.post(
        f"/assignments/{assignment_id}/otp/verify",
        headers={"Authorization": f"Bearer {doctor_token}"},
        params={"type": "checkin", "otp": otp, "lat": 13.04, "lng": 80.23},
    )
    assert verify.status_code == 200
    assert verify.json()["status"] == "checked_in"
