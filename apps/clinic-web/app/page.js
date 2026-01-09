"use client";

import { useEffect, useState } from "react";
import LiveMap from "../components/LiveMap";

export default function Home() {
  const [doctorLocation, setDoctorLocation] = useState({ lat: 13.05, lng: 80.24 });
  const [shiftDraft, setShiftDraft] = useState({
    specialty: "dentist_general",
    start_time: "2024-09-05T09:00",
    end_time: "2024-09-05T13:00",
    pay_amount: 4500,
    address: "T Nagar, Chennai",
    notes: "Bring toolkit",
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setDoctorLocation((prev) => ({
        lat: prev.lat + (Math.random() - 0.5) * 0.001,
        lng: prev.lng + (Math.random() - 0.5) * 0.001,
      }));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main>
      <section className="sidebar">
        <div className="card">
          <h2>LocumMap Chennai</h2>
          <p className="status-chip en-route">Live Shift</p>
          <h3>Dr. Anya Rao</h3>
          <p>Endodontist • ETA 12 mins</p>
        </div>
        <div className="card">
          <h3>Post a shift</h3>
          <label>
            Specialty
            <select
              className="input"
              value={shiftDraft.specialty}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, specialty: event.target.value })
              }
            >
              <option value="dentist_general">Dentist (General)</option>
              <option value="endodontist">Endodontist</option>
              <option value="anesthetist">Anesthetist</option>
            </select>
          </label>
          <label>
            Start time
            <input
              type="datetime-local"
              className="input"
              value={shiftDraft.start_time}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, start_time: event.target.value })
              }
            />
          </label>
          <label>
            End time
            <input
              type="datetime-local"
              className="input"
              value={shiftDraft.end_time}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, end_time: event.target.value })
              }
            />
          </label>
          <label>
            Pay (₹)
            <input
              type="number"
              className="input"
              value={shiftDraft.pay_amount}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, pay_amount: event.target.value })
              }
            />
          </label>
          <label>
            Address
            <input
              className="input"
              value={shiftDraft.address}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, address: event.target.value })
              }
            />
          </label>
          <label>
            Notes
            <input
              className="input"
              value={shiftDraft.notes}
              onChange={(event) =>
                setShiftDraft({ ...shiftDraft, notes: event.target.value })
              }
            />
          </label>
          <button className="primary-btn">Publish shift</button>
        </div>
        <div className="card">
          <h4>Live status</h4>
          <p className="status-chip checked-in">Checked-in</p>
          <p>OTP verified • 09:05 AM</p>
        </div>
      </section>
      <section className="map-container">
        <LiveMap doctorLocation={doctorLocation} />
        <div className="bottom-sheet">
          <strong>On shift now</strong>
          <p>Sunny Dental Clinic • 10:00 AM - 2:00 PM</p>
          <button className="primary-btn">Contact doctor</button>
        </div>
      </section>
    </main>
  );
}
