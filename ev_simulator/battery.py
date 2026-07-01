"""
Battery pack model.

Tracks state of charge (SOC) as electrical power is drawn (discharge)
or returned (regenerative braking charge).
"""


class Battery:
    def __init__(self, capacity_kwh=3.0, nominal_voltage=48.0,
                 internal_resistance=0.05, initial_soc=1.0):
        self.capacity_kwh = capacity_kwh
        self.capacity_wh = capacity_kwh * 1000.0
        self.nominal_voltage = nominal_voltage
        self.internal_resistance = internal_resistance
        self.soc = initial_soc  # fraction, 0.0 - 1.0

        self.energy_used_wh = 0.0    # cumulative discharge
        self.energy_regen_wh = 0.0   # cumulative regen charge

    def draw_power(self, power_w, dt_s):
        """
        Draw `power_w` watts of electrical power for `dt_s` seconds.

        power_w > 0  -> discharging the battery (propulsion)
        power_w < 0  -> charging the battery (regenerative braking)

        Returns the updated SOC (0.0 - 1.0).
        """
        energy_wh = power_w * dt_s / 3600.0

        if energy_wh >= 0:
            self.energy_used_wh += energy_wh
            self.soc -= energy_wh / self.capacity_wh
        else:
            charge_wh = -energy_wh
            self.energy_regen_wh += charge_wh
            self.soc += charge_wh / self.capacity_wh

        self.soc = max(0.0, min(1.0, self.soc))
        return self.soc

    def remaining_energy_wh(self):
        return self.soc * self.capacity_wh
