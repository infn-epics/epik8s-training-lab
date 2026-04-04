# epik8s-opi

Unified OPI interfaces and scripts for SPARC beamline controls, providing generic and reusable graphical panels for diagnostics, magnets, motors, vacuum, cooling, and other device groups. This repository is designed to work with the EPIK8S deployment and configuration system.

## Overview

The `epik8s-opi` package contains:

- **Generic OPI panels** for device groups (e.g., cooling, vacuum, magnets, motors, cameras)
- **Jython scripts** for dynamic population of OPI panels from YAML configuration files
- **Macro-driven configuration** for flexible reuse across different devices and beamlines

## Structure

- `unicool-opi/` — Unified cooling channel OPI and scripts
- `univac-opi/` — Unified vacuum channel OPI and scripts
- `unimag-opi/` — Unified magnet channel OPI and scripts
- `unimot-opi/` — Unified motor channel OPI and scripts
- `Scripts/` — Jython scripts for dynamic OPI population
- `resources/` — Shared OPI widgets and templates

## Generic OPI Interfaces

Each device group (cooling, vacuum, magnet, motor, etc.) provides a generic OPI panel (e.g., `cool_channel.bob`, `vac_channel.bob`, `mag_channel.bob`, `mot_channel.bob`) that uses macros to display and control device-specific PVs. These panels are designed to be embedded and reused for multiple devices.

### Example: Cooling Channel OPI (`cool_channel.bob`)

- **Macros:** `P`, `R`, `NAME`, `ZONE`, `OPI`, `LCID`
- **PVs:**  
  - `$(P):$(R):TEMP_RB` — Temperature readback  
  - `$(P):$(R):TEMP_SP` — Temperature setpoint  
  - `$(P):$(R):STATE_RB` — Status readback  
  - `$(P):$(R):STATE_SP` — Status setpoint  
- **Possible States:** `OFF`, `ON`, `STANDBY`, `FAULT`, `MAINTENANCE`

### Example: Vacuum Channel OPI (`vac_channel.bob`)

- **Macros:** `P`, `R`, `NAME`, `ZONE`, `TYPE`, `OPI`, `LCID`
- **PVs:**  
  - `$(P):$(R):PRES_RB` — Pressure readback  
  - Sensor type and zone displayed via macros

### Example: Magnet Channel OPI (`mag_channel.bob`)

- **Macros:** `P`, `R`, `NAME`, `ZONE`, `OPI`, `LCID`
- **PVs:**  
  - `$(P):$(R):CURRENT_RB` — Current readback  
  - `$(P):$(R):CURRENT_SP` — Current setpoint  
  - `$(P):$(R):STATE_RB` — Status readback  
  - `$(P):$(R):STATE_SP` — Status setpoint  
- **Possible States:** `OFF`, `ON`, `STANDBY`, `FAULT`, `RESET`

### Example: Motor Channel OPI (`mot_channel.bob`)

- **Macros:** `P`, `R`, `NAME`, `ZONE`, `TYPE`, `OPI`
- **PVs:**  
  - `$(P):$(R):RBV` — Position readback  
  - `$(P):$(R):VAL_SP` — Position setpoint  
  - `$(P):$(R):CMD` — Command PV  
  - Status bits and action PVs for motor control

## Dynamic OPI Population Scripts

The `Scripts/YAMLLoadDevicePopulateArray.py` script enables dynamic population of OPI panels based on the device configuration in a YAML file (typically `values.yaml` from the EPIK8S chart). The script:

- Loads device definitions from the YAML configuration
- Filters devices by group, zone, and type
- Creates embedded OPI widgets for each device, passing macros for PV mapping

**Usage:**  
Set the `CONFFILE` macro to the YAML configuration file and the `GROUP` macro to the device group (e.g., `unicool`, `univac`, `unimag`). The script will automatically generate the appropriate OPI panels for each device.

## How to Use

1. **Configure macros** in your OPI display to select the device group, configuration file, and other parameters.
2. **Embed the generic channel OPI** (e.g., `cool_channel.bob`) for each device, passing the correct macros.
3. **Use the provided scripts** to auto-populate device panels from the YAML configuration.

## Integration with EPIK8S

These OPIs and scripts are designed to work with the EPIK8S Helm chart and configuration system. Device definitions in `values.yaml` are automatically mapped to OPI panels, enabling a unified and maintainable control interface for the SPARC beamline.

## Documentation

- See each device group's README for details on PVs and macros.
- Refer to the comments in `YAMLLoadDevicePopulateArray.py` for script usage.
- For more information on EPIK8S configuration, see the main chart documentation.
