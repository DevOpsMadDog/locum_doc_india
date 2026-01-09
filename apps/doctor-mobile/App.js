import { useEffect, useState } from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import * as Location from "expo-location";

export default function App() {
  const [status, setStatus] = useState("Booked");
  const [location, setLocation] = useState(null);

  useEffect(() => {
    const subscribe = async () => {
      const { status: permission } = await Location.requestForegroundPermissionsAsync();
      if (permission !== "granted") {
        return;
      }
      const { status: bgStatus } = await Location.requestBackgroundPermissionsAsync();
      if (bgStatus === "granted") {
        await Location.startLocationUpdatesAsync("locum-tracking", {
          accuracy: Location.Accuracy.High,
          timeInterval: 15000,
          distanceInterval: 10,
        });
      }
      const current = await Location.getCurrentPositionAsync({});
      setLocation(current.coords);
    };
    subscribe();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>LocumMap Doctor</Text>
      <View style={styles.card}>
        <Text style={styles.chip}>{status}</Text>
        <Text style={styles.subtitle}>Upcoming shift • Sunny Dental Clinic</Text>
        <Text style={styles.body}>10:00 AM - 2:00 PM</Text>
        <TouchableOpacity style={styles.primary} onPress={() => setStatus("En Route")}> 
          <Text style={styles.primaryText}>Start navigation</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.card}>
        <Text style={styles.subtitle}>Live location</Text>
        {location ? (
          <Text style={styles.body}>
            {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
          </Text>
        ) : (
          <Text style={styles.body}>Waiting for GPS...</Text>
        )}
        <TouchableOpacity style={styles.secondary} onPress={() => setStatus("Checked In")}>
          <Text style={styles.secondaryText}>Check-in with OTP</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.secondary} onPress={() => setStatus("Completed")}>
          <Text style={styles.secondaryText}>Check-out</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: "#f3f6fb",
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    marginBottom: 16,
    color: "#0b1220",
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 12,
  },
  chip: {
    alignSelf: "flex-start",
    backgroundColor: "#dbeafe",
    color: "#1d4ed8",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    fontSize: 12,
    fontWeight: "600",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    fontWeight: "600",
  },
  body: {
    fontSize: 14,
    color: "#6b7280",
    marginVertical: 8,
  },
  primary: {
    backgroundColor: "#1d4ed8",
    padding: 12,
    borderRadius: 12,
    marginTop: 8,
  },
  primaryText: {
    color: "#ffffff",
    fontWeight: "600",
    textAlign: "center",
  },
  secondary: {
    backgroundColor: "#e5e7eb",
    padding: 10,
    borderRadius: 12,
    marginTop: 8,
  },
  secondaryText: {
    textAlign: "center",
    color: "#111827",
    fontWeight: "600",
  },
});
