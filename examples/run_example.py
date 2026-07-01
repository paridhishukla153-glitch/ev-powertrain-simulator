"""
Example: run the simulator once, print a summary, and run a battery-capacity
sensitivity sweep -- reproduces the kind of trade-off table an EV design
engineer would generate during a feasibility study.

Run:  python examples/run_example.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ev_simulator.simulate import run_simulation, sensitivity_sweep


def main():
    result = run_simulation(
        battery_capacity_kwh=3.0,
        vehicle_mass_kg=150,
        motor_power_w=3000,
    )

    print("=== Baseline Simulation ===")
    print(f"Distance simulated : {result['distance_km']:.2f} km")
    print(f"Energy used         : {result['energy_used_kwh']:.3f} kWh")
    print(f"Energy regenerated  : {result['energy_regen_kwh']:.3f} kWh")
    print(f"Consumption         : {result['consumption_wh_per_km']:.1f} Wh/km")
    print(f"Estimated range     : {result['estimated_range_km']:.1f} km")
    print(f"Regen recovery      : {result['regen_recovery_pct']:.1f} %")

    print("\n=== Sensitivity: Battery Capacity vs Range ===")
    for cap, rng in sensitivity_sweep("battery_capacity_kwh", [1, 2, 3, 4, 5, 6, 7, 8]):
        print(f"  {cap:>4.1f} kWh -> {rng:>6.1f} km")

    print("\n=== Sensitivity: Vehicle Mass vs Consumption ===")
    for mass in [100, 150, 200, 250, 300]:
        r = run_simulation(vehicle_mass_kg=mass)
        print(f"  {mass:>4d} kg -> {r['consumption_wh_per_km']:>6.1f} Wh/km")


if __name__ == "__main__":
    main()
