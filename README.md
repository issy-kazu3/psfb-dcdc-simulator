# psfb-dcdc-simulator
PSFB DC-DC converter simulator in Python with nonlinear magnetic component models. Migrated from a legacy VBA tool.

![Outlook](https://github.com/issy-kazu3/psfb-dcdc-simulator/blob/main/images/github.png)

# PSFB DC-DC Simulator

A Python implementation of a PSFB (Phase Shift Full Bridge)

DC-DC converter simulator. 

# Background & Purpose
This tool was originally developed 13 years ago as a VBA-based design script and has now been fully migrated to Python. Beyond numerical calculation, it is designed to serve as an interactive tutorial for engineers and students learning about PSFB DC-DC converters, switch timing, and nonlinear magnetic component modeling through L-I characteristic tables. 

![L-I](https://github.com/issy-kazu3/psfb-dcdc-simulator/blob/main/images/L-I.png)

 

# Features
 

- **PSFB steady-state waveform calculation**
- **Normalized $L-I$ characteristics (1-turn trans core self-inductance):** Simulates ripple waveforms based on standardized trans-core $L-I$ data under custom primary turns, voltage, current, and switching parameters.
- **Nonlinear magnetic modeling:** Visualizes ripple current distortion caused by core nonlinearity and saturation.
- **Magnetizing current observation:** Calculates and displays transformer magnetizing current.
- **Switch timing visualization:** Clear graphical output for understanding phase-shift timing.
- **CSV-based component data:** Easy import of custom magnetic core characteristics.
- **GUI interface:** User-friendly GUI implementation in Python.
