"""
Electric motor + inverter model.

Simplified constant-efficiency model (BLDC/PMSM + inverter combined).
This is the same first-pass abstraction used in early-stage EV
feasibility studies before a full torque-speed efficiency map exists.
"""


class Motor:
    def __init__(self, rated_power_w=3000, peak_efficiency=0.90,
                 inverter_efficiency=0.95):
        self.rated_power_w = rated_power_w
        self.peak_efficiency = peak_efficiency
        self.inverter_efficiency = inverter_efficiency
        self.combined_efficiency = peak_efficiency * inverter_efficiency

    def electrical_power_for(self, mechanical_power_w):
        """
        Convert a mechanical power demand (at the motor shaft) into the
        electrical power that must be drawn from (or returned to) the battery.

        mechanical_power_w > 0 -> propulsion, draws MORE electrical power
                                   than mechanical power (losses)
        mechanical_power_w < 0 -> braking/regen, RETURNS LESS electrical
                                   power than the mechanical energy available
        """
        if mechanical_power_w >= 0:
            return mechanical_power_w / self.combined_efficiency
        else:
            return mechanical_power_w * self.combined_efficiency
