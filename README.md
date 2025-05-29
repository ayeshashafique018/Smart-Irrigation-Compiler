# SISL Compiler - Smart Irrigation Scheduling Language

## Overview

The **SISL Compiler** is a tool for automating irrigation scheduling in agriculture and landscaping. It enables users to define efficient watering schedules using the **Smart Irrigation Scheduling Language (SISL)**, taking into account soil moisture, weather forecasts, crop type, and time of day. The compiler validates schedules, ensures efficient water usage, and generates low-level commands for irrigation controllers.

---

## Features

- **Parsing**: Recognizes sensor declarations, weather inputs, irrigation zones, and schedules.
- **Symbol Table**: Manages sensor types, zones, and environmental variables.
- **Semantic Analysis**: Validates sensor thresholds, watering durations, and time formats.
- **Code Generation**: Converts SISL commands into actionable code for irrigation controllers.

---

## Installation

Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/yourusername/SISL-Compiler-Engine.git
cd SISL-Compiler-Engine
