import "../styles/globals.css";

export const metadata = {
  title: "LocumMap Chennai | Clinic",
  description: "Clinic dashboard for LocumMap Chennai",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
