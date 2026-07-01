# Step-by-Step Build Guide: EV Powertrain Simulator

Written the way you'd actually scope this at Cummins/TVS: define the physics first, build bottom-up, validate each block in isolation, then integrate.

The finished code for every step below already exists in this repo — this guide explains *why* it's structured that way, so you can defend every design decision in an interview and extend it confidently.

---

## Step 0 — Scope the model before writing code

Decide what you're modeling and what you're deliberately ignoring. Being explicit about this is what separates an engineering project from a toy script.

**In scope:** longitudinal dynamics (straight-line driving), constant-efficiency motor/inverter, SOC-based battery, regenerative braking, a representative urban drive cycle.

**Out of scope (state this in your README, don't hide it):** thermal effects, torque-speed efficiency maps, cornering/lateral dynamics, battery aging/degradation, real logged drive-cycle data.

This scoping is itself a skill recruiters look for — knowing what to model and what to defer.

## Step 1 — Set up the repo skeleton

```bash
mkdir ev-powertrain-simulator && cd ev-powertrain-simulator
git init
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
mkdir ev_simulator tests examples
```

Create `requirements.txt` up front (`numpy`, `matplotlib`, `streamlit`, `pytest`) so environment setup is reproducible from commit #1.

## Step 2 — Battery model first (it's the simplest, and everything else feeds into it)

`ev_simulator/battery.py` tracks state of charge (SOC) as a fraction 0–1. The only operation it needs is `draw_power(power_w, dt_s)`:

- Positive power → discharge → SOC drops
- Negative power → regen charge → SOC rises
- Clamp SOC to [0, 1] so you never get a nonsensical negative-fuel result

**Validate in isolation** before moving on: drawing 1000 W for 3600 s from a 1 kWh battery should leave SOC at exactly 0. This is the kind of unit check that catches unit-conversion bugs (Wh vs kWh vs J) early, where they're cheap to fix.

## Step 3 — Vehicle dynamics (the physics core)

`ev_simulator/vehicle.py` computes wheel power from the classic longitudinal equation:

```
P_wheel = (F_aero + F_rolling + F_grade + F_accel) · v
```

Build and test each force term separately:
- `F_aero` should scale with v² — verify this with a quick script before integrating
- `F_rolling` should be roughly constant at cruise speed, small compared to aero drag at highway speed
- `F_accel` should dominate during hard acceleration phases

This decomposition is exactly what you'd sanity-check on a whiteboard before touching code, and it's the single most interview-worthy part of the project — be ready to explain why drag scales quadratically and rolling resistance doesn't.

## Step 4 — Motor + inverter losses

`ev_simulator/motor.py` converts mechanical power at the shaft to electrical power at the battery terminals, applying a combined efficiency (motor × inverter). Propulsion divides by efficiency (losses cost you more energy than the mechanical work delivered); regen multiplies by efficiency (you get back less than the kinetic energy available). Getting the direction of this asymmetry right is the most common bug in student EV models — test it explicitly.

## Step 5 — Drive cycle generator

Real WLTP/IDC cycles are licensed datasets, so `ev_simulator/drive_cycle.py` generates a synthetic stop-and-go urban profile: randomized accel/cruise/decel/idle phases with a capped top speed. This is disclosed clearly in the README — don't imply it's a certified test cycle when presenting the project.

If you later get access to a real logged GPS trace (e.g., your own commute logged via a phone app), swap it in here — the rest of the pipeline doesn't change.

## Step 6 — Wire it together in the simulation loop

`ev_simulator/simulate.py` is the only file that knows about all four other modules. Per timestep: vehicle → wheel power → motor → electrical power → battery → updated SOC. Accumulate distance, energy used, and energy regenerated; stop early if SOC hits 0 (that's your range).

Keep this loop dumb — no physics lives here, only orchestration. If you need to change a physics assumption, you should never have to touch `simulate.py`.

## Step 7 — Sensitivity analysis (the differentiator)

Add a `sensitivity_sweep(param_name, values)` helper that reruns the simulation once per value of any parameter, holding everything else fixed. This is what turns "I built a simulator" into "I performed trade-off analysis" — the exact language that separates this from a hobby project.

## Step 8 — Test everything

`tests/test_simulator.py` covers each module's core invariant: discharge lowers SOC, regen raises it, SOC stays in bounds, propulsion costs more than it delivers, higher battery capacity increases range monotonically. Run `pytest -v` locally before every commit.

## Step 9 — Build the dashboard

`app.py` (Streamlit) exposes every design parameter as a slider, runs the simulation live, and plots speed/SOC/power traces plus a range-vs-battery-capacity sensitivity chart. This is what a non-technical interviewer can actually click through in 30 seconds — it does more for you than the code itself.

## Step 10 — CI, so the repo proves itself

`.github/workflows/ci.yml` installs dependencies and runs `pytest` on every push to `main`. A green checkmark on your repo is a small thing that quietly signals "this person ships working code," without you having to say it.

## Step 11 — Ship it

```bash
git add .
git commit -m "Initial commit: EV powertrain simulator"
git branch -M main
git remote add origin https://github.com/<you>/ev-powertrain-simulator.git
git push -u origin main
```

Then deploy the dashboard for free on [share.streamlit.io](https://share.streamlit.io) (point it at `app.py`), and paste the live URL at the top of your README.

## Step 12 — Polish for portfolio

- Add 2–3 screenshots of the dashboard to the README
- Record a 20-second screen-capture GIF of the sliders in action
- Write one paragraph in the README explaining what's *out of scope* (Step 0) — this reads as senior-level honesty, not a weakness
- Pin the repo on your GitHub profile

---

## What to say in an interview

> "I built a Python-based EV powertrain simulator that models battery behavior, vehicle dynamics, motor/inverter losses, and regenerative braking under a synthetic Indian urban drive cycle. I ran sensitivity analysis on battery capacity, vehicle mass, and drag coefficient, backed it with unit tests and CI, and deployed it as a live dashboard."

Be ready for the natural follow-up: *"What would you add if this were a real product?"* — answer with Step 0's out-of-scope list (thermal effects, real drive-cycle data, torque-speed maps). Knowing your model's limits is more convincing than pretending it has none.
