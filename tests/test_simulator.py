"""Unit tests for the EV powertrain simulator."""
import numpy as np

from ev_simulator.battery import Battery
from ev_simulator.motor import Motor
from ev_simulator.vehicle import Vehicle
from ev_simulator.simulate import run_simulation, sensitivity_sweep


def test_battery_discharge_reduces_soc():
    b = Battery(capacity_kwh=1.0, initial_soc=1.0)
    soc = b.draw_power(power_w=1000, dt_s=3600)  # 1 kWh drawn over 1 hour
    assert abs(soc - 0.0) < 1e-6


def test_battery_regen_increases_soc():
    b = Battery(capacity_kwh=1.0, initial_soc=0.5)
    soc = b.draw_power(power_w=-500, dt_s=3600)  # 0.5 kWh regenerated
    assert soc > 0.5


def test_battery_soc_clamped_between_0_and_1():
    b = Battery(capacity_kwh=1.0, initial_soc=0.99)
    soc = b.draw_power(power_w=-10000, dt_s=3600)
    assert soc <= 1.0
    b2 = Battery(capacity_kwh=1.0, initial_soc=0.01)
    soc2 = b2.draw_power(power_w=10000, dt_s=3600)
    assert soc2 >= 0.0


def test_motor_propulsion_draws_more_than_mechanical():
    m = Motor(peak_efficiency=0.9, inverter_efficiency=0.95)
    elec = m.electrical_power_for(1000)
    assert elec > 1000


def test_motor_regen_returns_less_than_mechanical():
    m = Motor(peak_efficiency=0.9, inverter_efficiency=0.95)
    elec = m.electrical_power_for(-1000)
    assert elec > -1000  # less negative = less energy returned than available


def test_vehicle_power_increases_with_speed():
    v = Vehicle()
    p_low = v.required_wheel_power_w(speed_mps=5, accel_mps2=0)
    p_high = v.required_wheel_power_w(speed_mps=15, accel_mps2=0)
    assert p_high > p_low


def test_run_simulation_returns_sane_outputs():
    result = run_simulation(duration_s=300, battery_capacity_kwh=3.0)
    assert result["distance_km"] >= 0
    assert 0 <= result["energy_used_kwh"]
    assert not np.isnan(result["estimated_range_km"]) or result["distance_km"] == 0


def test_higher_battery_capacity_increases_range():
    r_small = run_simulation(battery_capacity_kwh=2.0, duration_s=600)
    r_large = run_simulation(battery_capacity_kwh=6.0, duration_s=600)
    assert r_large["estimated_range_km"] >= r_small["estimated_range_km"]


def test_sensitivity_sweep_returns_expected_length():
    values = [1, 2, 3]
    results = sensitivity_sweep("battery_capacity_kwh", values, base_kwargs={"duration_s": 300})
    assert len(results) == len(values)
