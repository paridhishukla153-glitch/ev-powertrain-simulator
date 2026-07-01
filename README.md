# EV Powertrain Simulator

A simple physics-based EV simulator built to understand how battery size, vehicle mass, regenerative braking, and driving conditions affect range and energy consumption.

The idea behind this project was straightforward: EV brochures advertise range numbers, but I wanted to understand how those numbers are actually estimated and which vehicle parameters influence them the most.

## Features

* Battery State of Charge (SOC) tracking
* Motor and inverter efficiency losses
* Regenerative braking model
* Rolling resistance and aerodynamic drag calculations
* Urban stop-and-go drive cycle simulation
* Interactive dashboard for parameter exploration
* Automated unit tests and CI pipeline

## Project Structure

```text
ev-powertrain-simulator/
│
├── battery.py        # Battery and SOC model
├── motor.py          # Motor and inverter losses
├── vehicle.py        # Vehicle dynamics calculations
├── drive_cycle.py    # Speed profile generation
├── simulate.py       # Main simulation engine
├── app.py            # Streamlit dashboard
│
├── tests/            # Unit tests
├── requirements.txt
└── README.md
```

## What is being modeled?

### Battery

The battery model keeps track of available energy and state of charge throughout the drive cycle.

### Vehicle Dynamics

The simulator estimates the power required to move the vehicle by considering:

* Rolling resistance
* Aerodynamic drag
* Vehicle acceleration

### Motor and Inverter

The motor model includes efficiency losses during propulsion and energy recovery during braking.

### Regenerative Braking

During deceleration, a portion of kinetic energy is recovered and returned to the battery instead of being lost as heat.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

## Why I Built This

As an Electrical and Electronics Engineering student interested in EV systems and power electronics, I wanted a project that connects concepts such as energy storage, motor efficiency, and power flow with a practical application.

This simulator is not intended to replace professional tools such as MATLAB/Simulink or commercial vehicle simulation software. The goal is to build intuition about EV behavior and understand the trade-offs involved in vehicle design.

## Current Limitations

* Uses a synthetic urban drive cycle rather than standardized testing cycles.
* Uses simplified efficiency assumptions instead of full torque-speed maps.
* Does not currently model battery temperature effects.

## Future Improvements

* Battery thermal model
* Charging simulation
* Torque-speed efficiency maps
* Multiple vehicle categories (scooter, motorcycle, car)

## License

MIT License
