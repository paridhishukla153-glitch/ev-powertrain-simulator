# 🔋 EV Powertrain Simulator

A physics-based Python simulation of an electric vehicle drivetrain — battery, motor/inverter, vehicle dynamics, and regenerative braking — with an interactive dashboard and design sensitivity analysis.

> Built to answer the question a real EV design engineer asks: **"What happens if I change the design?"** — not just "can I build this?"

**[Live Demo](#deployment) · [Quick Start](#quick-start) · [Architecture](#architecture) · [Physics Model](#physics-model)**

---

## What it does

Given vehicle mass, battery capacity, motor rating, and aerodynamic properties, the simulator computes:

- **Range** under a synthetic Indian urban driving cycle
- **Energy consumption** (Wh/km)
- **Battery SOC trajectory** over time
- **Regenerative braking recovery** (%)
- **Sensitivity** of any of the above to any design parameter

```
Battery Capacity = 3 kWh
Vehicle Mass     = 150 kg
Motor Power      = 3 kW

Result:
Range              = 128.9 km
Energy Consumption = 23.3 Wh/km
Regen Recovery     = 14.0 %
```

## Architecture

```
Battery ⇄ Inverter ⇄ Motor ⇄ Drivetrain ⇄ Wheels ⇄ Vehicle (mass, drag, rolling resistance)
   ↑                                          |
   └──────────── Regenerative Braking ────────┘
```

```
ev-powertrain-simulator/
├── ev_simulator/
│   ├── battery.py       # SOC tracking, charge/discharge
│   ├── motor.py         # Motor + inverter efficiency losses
│   ├── vehicle.py        # Longitudinal dynamics: aero drag, rolling resistance, inertia
│   ├── drive_cycle.py    # Synthetic Indian urban drive cycle generator
│   └── simulate.py       # Simulation loop + sensitivity sweep utility
├── app.py                 # Streamlit interactive dashboard
├── examples/run_example.py
├── tests/test_simulator.py
└── .github/workflows/ci.yml
```

## Physics model

**Vehicle dynamics** — power required at the wheels:

```
F_total = F_aero + F_rolling + F_grade + F_accel
F_aero     = 0.5 · ρ_air · Cd · A · v²
F_rolling  = Crr · m · g · cos(θ)
F_grade    = m · g · sin(θ)
F_accel    = m · a

P_wheel = F_total · v
```

**Motor + inverter** — electrical power drawn from the battery:

```
P_elec = P_mech / (η_motor · η_inverter)      (propulsion)
P_elec = P_mech · (η_motor · η_inverter)       (regen — less energy recovered than dissipated)
```

**Battery** — SOC update per timestep:

```
ΔSOC = (P_elec · Δt / 3600) / capacity_Wh
SOC(t+1) = clamp(SOC(t) - ΔSOC, 0, 1)
```

This is the same first-pass abstraction used in early-stage EV feasibility studies, before a full torque-speed efficiency map and thermal model exist.

## Quick start

```bash
git clone https://github.com/<your-username>/ev-powertrain-simulator.git
cd ev-powertrain-simulator
pip install -r requirements.txt

# Run a one-off simulation + sensitivity sweep in the terminal
python examples/run_example.py

# Launch the interactive dashboard
streamlit run app.py

# Run the test suite
pytest -v
```

## Design trade-off examples

| Change | Effect |
|---|---|
| Battery 3 kWh → 5 kWh | Range 129 km → 215 km |
| Mass +50 kg | Consumption 23.3 → 26.5 Wh/km |
| Higher regen efficiency | Recovery 14% → up to ~25% |
| Higher drag coefficient | Range drops disproportionately at highway speed |

Run `python examples/run_example.py` to reproduce these sweeps with your own parameters, or use the sliders in the dashboard.

## Deployment

**Streamlit Community Cloud (free, ~2 minutes):**

1. Push this repo to GitHub (see [Shipping to GitHub](#shipping-to-github) below).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app** → select this repo → main file path `app.py` → **Deploy**.
4. You'll get a public URL like `https://<your-app>.streamlit.app` — put it in this README and on your resume/LinkedIn.

## Shipping to GitHub

```bash
cd ev-powertrain-simulator
git init
git add .
git commit -m "Initial commit: EV powertrain simulator"
git branch -M main
git remote add origin https://github.com/<your-username>/ev-powertrain-simulator.git
git push -u origin main
```

GitHub Actions CI (`.github/workflows/ci.yml`) will automatically run the test suite on every push.

## Roadmap / extension ideas

- Replace synthetic drive cycle with a real logged GPS trace (Indian city commute)
- Replace constant motor efficiency with a torque-speed efficiency map
- Add thermal derating (battery/motor performance vs ambient temperature)
- Add a cost model (₹/km) using current electricity tariffs
- Multi-cycle comparison (city vs highway vs mixed)

## Resume / interview framing

> "I built a Python-based EV powertrain simulator that models battery behavior, vehicle dynamics, motor/inverter losses, and regenerative braking under a synthetic Indian urban drive cycle. I ran sensitivity analysis across battery capacity, vehicle mass, and drag coefficient to quantify range and efficiency trade-offs, with full test coverage and CI, deployed as a live interactive dashboard."

## License

MIT — see [LICENSE](LICENSE).
