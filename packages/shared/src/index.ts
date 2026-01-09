export const SPECIALTIES = [
  "dentist_general",
  "endodontist",
  "anesthetist",
] as const;

export type Specialty = (typeof SPECIALTIES)[number];

export type ShiftStatus =
  | "draft"
  | "posted"
  | "booked"
  | "en_route"
  | "checked_in"
  | "completed"
  | "paid"
  | "canceled"
  | "no_show";

export interface Shift {
  id: number;
  specialty: Specialty;
  start_time: string;
  end_time: string;
  pay_amount: number;
  address: string;
  lat: number;
  lng: number;
  status: ShiftStatus;
}
