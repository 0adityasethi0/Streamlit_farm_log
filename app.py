import streamlit as st
import requests
from datetime import date, datetime

st.set_page_config(page_title="Farm Log Entry", layout="wide")
st.title("🌾 Daily Farm Log Entry")

# ---------- Today's Date and time ----------
entry_date = date.today()
entry_time = datetime.now()
st.markdown(f"📅 **Entry Date and Time**: `{entry_time}`")
st.markdown("---")

# ---------- Crop Info Section ----------
with st.expander("🌱 Crop & Labour Details", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        crop_name = st.selectbox("Crop Name", [
            "Blueberry 4.5", "Blueberry 6.5", "Raspberry",
            "Polyhouse Nursery", "Polytunnel", "Net House"
        ])
        activity = st.text_area("Activity Performed")

    with c2:
        labour_working_per_plant = st.number_input("👷 Labour per Plant", min_value=0)
        canteen = st.text_input("🍴 Canteen")

# ---------- Environment Data ----------
with st.expander("🌤️ Environment Data", expanded=False):
    e1, e2, e3 = st.columns(3)
    with e1:
        max_temp = st.number_input("Max Temp (°C)")
        min_temp = st.number_input("Min Temp (°C)")
    with e2:
        rainfall_mm = st.number_input("Rainfall (mm)")
        cumulative_rainfall_mm = st.number_input("Cumulative Rainfall (mm)")
    with e3:
        max_humidity = st.number_input("Max Humidity (%)")
        min_humidity = st.number_input("Min Humidity (%)")

# ---------- Irrigation & Nutrition ----------
with st.expander("💧 Irrigation & Fertilizer", expanded=False):
    i1, i2, i3 = st.columns(3)
    with i1:
        irrigation_volume = st.number_input("Irrigation Volume (L)")
    with i2:
        fertigation_volume = st.number_input("Fertigation Volume (L)")
    with i3:
        total_fertilizer_used = st.number_input("Total Fertilizer Used (kg)")

# ---------- Pest & Disease ----------
with st.expander("🪳 Pest and Disease Control", expanded=False):
    pest_col1, pest_col2 = st.columns(2)
    with pest_col1:
        Major_pest_observation = st.text_input("Major Pest Observation")
        pest_control_measure = st.text_input("Control Measure")
        pestiside_name = st.text_input("Pesticide Name")
    with pest_col2:
        dose_per_litre = st.number_input("Dose per Litre (ml)")
        total_volume_used = st.number_input("Total Volume Used (L)")
        Status_of_condition = st.text_input("Status of Condition")

# ---------- Fuel ----------
with st.expander("⛽ Fuel Consumption", expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        fuel_used_in_tractor1_big = st.number_input("Tractor 1 (Big) Fuel (L)")
        fuel_used_in_tractor2_small = st.number_input("Tractor 2 (Small) Fuel (L)")
    with f2:
        grass_cutter = st.number_input("Grass Cutter Fuel (L)")
        Auger_sprayer = st.number_input("Auger Sprayer Fuel (L)")
    with f3:
        Company_Bike = st.number_input("Company Bike Fuel (L)")
        miscellaneous = st.text_input("📝 Miscellaneous Notes")
        Total_petrol_used = st.number_input("Total Petrol Used (L)")
        Total_disel_used = st.number_input("Total Diesel Used (L)")

# ---------- Alerts ----------
with st.expander("🚨 System Alerts", expanded=True):
    if max_temp > 45:
        st.error("🌡️ Max Temperature is abnormally high!")
    if min_temp < 5:
        st.warning("❄️ Min Temperature is too low — possible frost risk.")
    if max_humidity > 95:
        st.warning("💧 Max Humidity very high — risk of fungal issues.")
    if rainfall_mm > 200:
        st.warning("🌧️ Heavy rainfall recorded — check field conditions.")
    if total_fertilizer_used > 50:
        st.warning("⚠️ High fertilizer usage — double-check dosage.")
    fuel_values = [
        fuel_used_in_tractor1_big,
        fuel_used_in_tractor2_small,
        grass_cutter,
        Auger_sprayer,
        Company_Bike
    ]
    if any(fuel > 100 for fuel in fuel_values):
        st.warning("⛽ High fuel usage detected in one or more machines.")

# ---------- Submit ----------
st.markdown("---")
if st.button("📤 Submit Entry"):
    try:
        payload = {
    "entry_date": str(entry_date),
    "entry_time": entry_time.isoformat(),
    "crop_name": crop_name,
    "activity": activity,
    "labour_working_per_plant": labour_working_per_plant,
    "canteen": canteen,
    "max_temp": max_temp,
    "min_temp": min_temp,
    "rainfall_mm": rainfall_mm,
    "cumulative_rainfall_mm": cumulative_rainfall_mm,
    "max_humidity": max_humidity,
    "min_humidity": min_humidity,
    "irrigation_volume": irrigation_volume,
    "fertigation_volume": fertigation_volume,
    "total_fertilizer_used": total_fertilizer_used,
    "Major_pest_observation": Major_pest_observation,
    "pest_control_measure": pest_control_measure,
    "pestiside_name": pestiside_name,
    "dose_per_litre": dose_per_litre,
    "total_volume_used": total_volume_used,
    "Status_of_condition": Status_of_condition,
    "fuel_used_in_tractor1_big": fuel_used_in_tractor1_big,
    "fuel_used_in_tractor2_small": fuel_used_in_tractor2_small,
    "grass_cutter": grass_cutter,
    "Auger_sprayer": Auger_sprayer,
    "Company_Bike": Company_Bike,
    "miscellaneous": miscellaneous,
    "Total_petrol_used": Total_petrol_used,
    "Total_disel_used": Total_disel_used
}

       # Send POST request to FastAPI
        response = requests.post("https://fastapi-farm-be.onrender.com/submit-entry", json=payload)

        if response.status_code == 200:
            st.success(response.json().get("message", "✅ Entry submitted successfully!"))
        else:
            st.error(f"❌ Submission failed. Status: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"❌ Error: {e}")
