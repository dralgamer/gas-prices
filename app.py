import requests
import streamlit as st

# Titel der Web-App
st.title("⛽ Spritpreise Schweinfurt & Dittelbrunn")
st.write("Hier siehst du die aktuellen Benzinpreise im Umkreis von 10 km.")

# Konfiguration
LAT = 50.0500
LNG = 10.2333
RADIUS = 10
API_KEY = "20b674cf-1280-483c-bbeb-969b33aac713"  # Trage hier deinen Key ein, sobald du ihn hast

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

                # Wir zeigen die Daten in einer schönen Tabelle oder Liste an
                for station in stations:
                    name = station.get("name")
                    brand = station.get("brand")
                    price = station.get("price")
                    isOpen = station.get("isOpen")

                    status = "🟢 Geöffnet" if isOpen else "🔴 Geschlossen"

                    # Jede Tankstelle als kleine Info-Box darstellen
                    st.markdown(f"**{brand}** ({name})")
                    st.write(preis_text := f"Preis: **{price} €** | Status: {status}")
                    st.divider()
            else:
                st.warning("Keine Tankstellen im angegebenen Radius gefunden.")
        else:
            st.error("Fehler beim Abrufen der Daten. Ist der API-Key korrekt?")

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")