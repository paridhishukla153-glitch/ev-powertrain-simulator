"""
Core simulation engine.

Ties together Battery + Motor + Vehicle + DriveCycle to answer the
questions a real EV feasibility study answers: range, consumption,
SOC trajectory, and regen recovery -- and lets you sweep any design
parameter to see the trade-off.
"""
import numpy as np

from .battery import Battery
from .motor import Motor
from .vehicle import Vehicle
from .drive_cycle import generate_indian_urban_cycle


def run_simulation(battery_capacity_kwh=3.0, vehicle_mass_kg=150, motor_power_w=3000,
                    drag_coeff=0.7, frontal_area_m2=0.6, rolling_resistance_coeff=0.015,
                    duration_s=1200, dt_s=1.0, max_speed_kmph=50, initial_soc=1.0,
                    seed=42):

    battery = Battery(capacity_kwh=battery_capacity_kwh, initial_soc=initial_soc)
    motor = Motor(rated_power_w=motor_power_w)
    vehicle = Vehicle(mass_kg=vehicle_mass_kg, frontal_area_m2=frontal_area_m2,
                       drag_coeff=drag_coeff, rolling_resistance_coeff=rolling_resistance_coeff)

    t, speed = generate_indian_urban_cycle(duration_s=duration_s, dt_s=dt_s,
                                            max_speed_kmph=max_speed_kmph, seed=seed)
    accel = np.gradient(speed, dt_s)

    distance_m = 0.0
    soc_trace, power_trace, distance_trace = [], [], []

    for i in range(len(t)):
        wheel_power = vehicle.required_wheel_power_w(speed[i], accel[i])
        motor_mech_power = vehicle.wheel_to_motor_power(wheel_power)
        elec_power = motor.electrical_power_for(motor_mech_power)
        soc = battery.draw_power(elec_power, dt_s)
        distance_m += speed[i] * dt_s

        soc_trace.append(soc)
        power_trace.append(elec_power)
        distance_trace.append(distance_m)

        if soc <= 0:
            break

    distance_km = distance_m / 1000.0
    energy_used_kwh = battery.energy_used_wh / 1000.0
    energy_regen_kwh = battery.energy_regen_wh / 1000.0
    net_energy_kwh = energy_used_kwh - energy_regen_kwh

    consumption_wh_per_km = (net_energy_kwh * 1000.0 / distance_km) if distance_km > 0 else float("nan")

    if distance_km > 0 and net_energy_kwh > 0:
        estimated_range_km = battery_capacity_kwh / (consumption_wh_per_km / 1000.0)
    else:
        estimated_range_km = float("nan")

    regen_recovery_pct = (energy_regen_kwh / energy_used_kwh * 100.0) if energy_used_kwh > 0 else 0.0

    return {
        "time_s": t[:len(soc_trace)],
        "speed_mps": speed[:len(soc_trace)],
        "soc_trace": np.array(soc_trace),
        "power_trace_w": np.array(power_trace),
        "distance_trace_m": np.array(distance_trace),
        "distance_km": distance_km,
        "energy_used_kwh": energy_used_kwh,
        "energy_regen_kwh": energy_regen_kwh,
        "net_energy_kwh": net_energy_kwh,
        "consumption_wh_per_km": consumption_wh_per_km,
        "estimated_range_km": estimated_range_km,
        "regen_recovery_pct": regen_recovery_pct,
    }


def sensitivity_sweep(param_name, values, base_kwargs=None):
    """
    Run the simulation once per value of `param_name`, holding all other
    parameters fixed. Returns a list of (value, estimated_range_km) tuples.

    Example:
        sensitivity_sweep("battery_capacity_kwh", [1, 2, 3, 4, 5])
    """
    base_kwargs = dict(base_kwargs or {})
    results = []
    for v in values:
        kwargs = dict(base_kwargs)
        kwargs[param_name] = v
        r = run_simulation(**kwargs)
        results.append((v, r["estimated_range_km"]))
    return results
