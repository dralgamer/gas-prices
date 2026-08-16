import requests
import streamlit as st

# Titel der Web-App
st.title("⛽ Spritpreise Schweinfurt & Dittelbrunn")
st.write("Hier siehst du die aktuellen Benzinpreise im Umkreis von 10 km.")

# Konfiguration
LAT = 50.0500
LNG = 10.2333
RADIUS = 10
API_KEY = "20b674cf-1280-483c-bbeb-969b33aac713"  # Trage hier deinen Key ein

url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={LAT}&lng={LNG}&rad={RADIUS}&sort=price&type=e5&apikey={API_KEY}"

# Einen Button hinzufügen, um die Preise zu aktualisieren
if st.button("Preise jetzt abrufen"):
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("ok"):
            stations = data.get("stations", [])

            if stations:
                st.success(f"Es wurden {len(stations)} Tankstellen gefunden:")

                # Jede Tankstelle durchgehen und anzeigen
                for station in stations:
                    name = station.get("name")
                    brand = station.get("brand")
                    price = station.get("price")
                    isOpen = station.get("isOpen")

                    # Koordinaten für Google Maps auslesen
                    lat_station = station.get("lat")
                    lng_station = station.get("lng")
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={lat_station},{lng_station}"

                    status = "🟢 Geöffnet" if isOpen else "🔴 Geschlossen"

                    # Ausgabe mit klickbarem Maps-Link im Tankstellennamen
                    st.markdown(f"### **[{brand} - {name}]({maps_url})**")
                    st.write(f"Preis: **{price} €** | Status: {status}")
                    st.markdown(f"[📍 Route zu dieser Tankstelle auf Google Maps öffnen]({maps_url})")
                    st.divider()
            else:
                st.warning("Keine Tankstellen im angegebenen Radius gefunden.")
        else:
            st.error("Fehler beim Abrufen der Daten. Ist der API-Key korrekt?")

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")