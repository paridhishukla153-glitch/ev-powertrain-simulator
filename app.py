"""
Streamlit dashboard for the EV Powertrain Simulator.

Run locally:      streamlit run app.py
Deploy for free:  push to GitHub -> connect repo on share.streamlit.io
"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


from ev_simulator.simulate import run_simulation

st.set_page_config(page_title="EV Powertrain Simulator", page_icon="🔋", layout="wide")

st.title("🔋 EV Powertrain Simulator")
st.caption("Battery • Motor & Inverter • Vehicle Dynamics • Regenerative Braking — "
           "modeled end-to-end, with live design trade-off analysis.")

st.sidebar.header("Simulation Parameters")

vehicle_type = st.sidebar.selectbox(
    "Vehicle Type",
    [
        "Electric Scooter",
        "Electric Motorcycle",
        "Passenger Car"
    ]
)

if vehicle_type == "Electric Scooter":
    default_battery = 3.0
    default_mass = 150
    default_power = 3000

elif vehicle_type == "Electric Motorcycle":
    default_battery = 6.0
    default_mass = 220
    default_power = 7000

else:
    default_battery = 40.0
    default_mass = 1400
    default_power = 90000

with st.sidebar:
    st.header("Design Parameters")
    battery_capacity_kwh = st.slider(
    "Battery Capacity (kWh)",
    1.0,
    50.0,
    float(default_battery),
    0.5
)
    vehicle_mass_kg = st.slider(
        "Vehicle Mass (kg)",
        80,
        2000,
        int(default_mass),
        10
    )

    motor_power_w = st.slider(
        "Motor Rated Power (W)",
        1000,
        100000,
        int(default_power),
        500
    )

    drag_coeff = st.slider("Drag Coefficient (Cd)", 0.3, 1.2, 0.7, 0.05)
    frontal_area_m2 = st.slider("Frontal Area (m²)", 0.3, 2.5, 0.6, 0.05)
    rolling_resistance_coeff = st.slider("Rolling Resistance Coeff.", 0.005, 0.03, 0.015, 0.001)
    max_speed_kmph = st.slider("Max Cycle Speed (km/h)", 20, 100, 50, 5)
    duration_s = st.slider("Drive Cycle Duration (s)", 300, 3600, 1200, 100)

result = run_simulation(
    battery_capacity_kwh=battery_capacity_kwh,
    vehicle_mass_kg=vehicle_mass_kg,
    motor_power_w=motor_power_w,
    drag_coeff=drag_coeff,
    frontal_area_m2=frontal_area_m2,
    rolling_resistance_coeff=rolling_resistance_coeff,
    duration_s=duration_s,
    max_speed_kmph=max_speed_kmph,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Estimated Range", f"{result['estimated_range_km']:.1f} km")
c2.metric("Consumption", f"{result['consumption_wh_per_km']:.1f} Wh/km")
c3.metric("Regen Recovery", f"{result['regen_recovery_pct']:.1f} %")
c4.metric("Distance Simulated", f"{result['distance_km']:.2f} km")

st.subheader("Drive Cycle, SOC and Power Trace")
fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
axes[0].plot(result["time_s"], result["speed_mps"] * 3.6)
axes[0].set_ylabel("Speed (km/h)")
axes[1].plot(result["time_s"], result["soc_trace"] * 100, color="green")
axes[1].set_ylabel("SOC (%)")
axes[2].plot(result["time_s"], result["power_trace_w"], color="orange")
axes[2].axhline(0, color="gray", linewidth=0.8)
axes[2].set_ylabel("Electrical Power (W)")
axes[2].set_xlabel("Time (s)")
fig.tight_layout()
st.pyplot(fig)

st.subheader("Sensitivity Analysis — Range vs Battery Capacity")
caps = np.linspace(1, 10, 10)
ranges = []
for c in caps:
    r = run_simulation(battery_capacity_kwh=c, vehicle_mass_kg=vehicle_mass_kg,
                        motor_power_w=motor_power_w, drag_coeff=drag_coeff,
                        frontal_area_m2=frontal_area_m2,
                        rolling_resistance_coeff=rolling_resistance_coeff,
                        duration_s=duration_s, max_speed_kmph=max_speed_kmph)
    ranges.append(r["estimated_range_km"])

fig2, ax2 = plt.subplots(figsize=(10, 3.5))
ax2.plot(caps, ranges, marker="o")
ax2.set_xlabel("Battery Capacity (kWh)")
ax2.set_ylabel("Estimated Range (km)")
ax2.grid(alpha=0.3)
fig2.tight_layout()
st.pyplot(fig2)

st.subheader("Sensitivity Analysis — Range vs Vehicle Mass")

masses = np.arange(100, 501, 25)
mass_ranges = []

for m in masses:
    r = run_simulation(
        battery_capacity_kwh=battery_capacity_kwh,
        vehicle_mass_kg=m,
        motor_power_w=motor_power_w,
        drag_coeff=drag_coeff,
        frontal_area_m2=frontal_area_m2,
        rolling_resistance_coeff=rolling_resistance_coeff,
        duration_s=duration_s,
        max_speed_kmph=max_speed_kmph,
    )

    mass_ranges.append(r["estimated_range_km"])

fig3, ax3 = plt.subplots(figsize=(10, 3.5))
ax3.plot(masses, mass_ranges, marker="o")
ax3.set_xlabel("Vehicle Mass (kg)")
ax3.set_ylabel("Estimated Range (km)")
ax3.grid(alpha=0.3)
fig3.tight_layout()

st.pyplot(fig3)

st.subheader("Typical Vehicle Comparison")

vehicles = ["Scooter", "Motorcycle", "Car"]
vehicle_ranges = [129, 185, 320]

fig4, ax4 = plt.subplots(figsize=(8, 4))
ax4.bar(vehicles, vehicle_ranges)
ax4.set_ylabel("Typical Range (km)")
ax4.set_title("Representative EV Range Comparison")
fig4.tight_layout()

st.pyplot(fig4)

st.subheader("Sensitivity Analysis — Range vs Vehicle Mass")

masses = np.arange(100, 2000, 100)
mass_ranges = []

for m in masses:
    r = run_simulation(
        battery_capacity_kwh=battery_capacity_kwh,
        vehicle_mass_kg=m,
        motor_power_w=motor_power_w,
        drag_coeff=drag_coeff,
        frontal_area_m2=frontal_area_m2,
        rolling_resistance_coeff=rolling_resistance_coeff,
        duration_s=duration_s,
        max_speed_kmph=max_speed_kmph
    )
    mass_ranges.append(r["estimated_range_km"])

fig3, ax3 = plt.subplots(figsize=(10, 3.5))
ax3.plot(masses, mass_ranges, marker="o")
ax3.set_xlabel("Vehicle Mass (kg)")
ax3.set_ylabel("Estimated Range (km)")
ax3.grid(alpha=0.3)
fig3.tight_layout()

st.pyplot(fig3)

st.caption("Built with a physics-based longitudinal vehicle dynamics model — "
           "not a lookup table")

st.divider()
st.header("About the Model")

with st.expander("Rolling Resistance"):
    st.write("""
Rolling resistance models tire deformation losses.

Force equation:

F_rr = C_rr × m × g
""")

with st.expander("Aerodynamic Drag"):
    st.write("""
Aerodynamic drag increases quadratically with speed.

Force equation:

F_drag = 0.5 × rho × Cd × A × v²
""")

with st.expander("Regenerative Braking"):
    st.write("""
During deceleration, part of the vehicle's kinetic energy
is recovered and returned to the battery.

Real EVs typically recover between 10% and 30%
of braking energy depending on conditions.
""")

with st.expander("Battery State of Charge"):
    st.write("""
Battery SOC is updated continuously based on
power consumption and recovered regenerative energy.
""")