# LIGGGHTS DEM Simulation of Vibrated Granular System

## Overview

This project simulates the dynamics of monodisperse particles under vertical vibration using **LIGGGHTS DEM**, and analyzes the resulting motion using Python.

The study focuses on:

* Center of mass motion
* Particle flight times
* Collision dynamics under sinusoidal forcing

## Structure

* `simulation/` – LIGGGHTS input script and STL geometries
* `analysis/` – Python scripts for post-processing
* `data/` – (optional) output data

## Requirements

* LIGGGHTS (Ubuntu/Linux)
* Python 3
* NumPy, Pandas, Matplotlib

## How to Run

### 1. Run Simulation

```bash
liggghts < input_script.in
```

### 2. Run Analysis

```bash
python analysis.py
```

## Notes

* STL files define the container geometry
* Log files are parsed and converted into CSV for analysis
* Flight times are computed using peak detection and thresholding
