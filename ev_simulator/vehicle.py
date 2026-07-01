"""
Longitudinal vehicle dynamics model.

Computes the power required at the wheels to achieve a given speed and
acceleration, accounting for aerodynamic drag, rolling resistance,
road grade, and inertial (acceleration) force.
"""
import math

G = 9.81
AIR_DENSITY = 1.225  # kg/m^3, sea level, 15C


class Vehicle:
    def __init__(self, mass_kg=150, frontal_area_m2=0.6, drag_coeff=0.7,
                 rolling_resistance_coeff=0.015, wheel_radius_m=0.28,
                 drivetrain_efficiency=0.96):
        self.mass_kg = mass_kg
        self.frontal_area_m2 = frontal_area_m2
        self.drag_coeff = drag_coeff
        self.rolling_resistance_coeff = rolling_resistance_coeff
        self.wheel_radius_m = wheel_radius_m
        self.drivetrain_efficiency = drivetrain_efficiency

    def required_wheel_power_w(self, speed_mps, accel_mps2, grade_rad=0.0):
        """Power required at the wheels (Watts) for the given speed/accel."""
        f_aero = 0.5 * AIR_DENSITY * self.drag_coeff * self.frontal_area_m2 * speed_mps ** 2
        f_roll = (self.rolling_resistance_coeff * self.mass_kg * G * math.cos(grade_rad)
                  if speed_mps > 0.1 else 0.0)
        f_grade = self.mass_kg * G * math.sin(grade_rad)
        f_accel = self.mass_kg * accel_mps2

        f_total = f_aero + f_roll + f_grade + f_accel
        return f_total * speed_mps

    def wheel_to_motor_power(self, wheel_power_w):
        """Account for gearbox / final-drive losses between motor and wheels."""
        if wheel_power_w >= 0:
            return wheel_power_w / self.drivetrain_efficiency
        else:
            return wheel_power_w * self.drivetrain_efficiency
