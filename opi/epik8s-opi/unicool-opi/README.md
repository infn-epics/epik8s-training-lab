# unicool-opi
unified view of chiller and cooling 


## PV Interface for `cool_channel.bob`

The `cool_channel.bob` OPI provides a unified interface for monitoring and controlling cooling channels. It uses the following Process Variables (PVs), which are parameterized via macros for flexibility:

- **Readout PV (`TEMP_RB`)**  
  Displays the current temperature readout for the channel.  
  PV format: `$(P):$(R):TEMP_RB`

- **Setpoint PV (`TEMP_SP`)**  
  Allows the user to set the desired temperature for the channel.  
  PV format: `$(P):$(R):TEMP_SP`

- **Status PV (`STATE_RB`)**  
  Shows the current status or state of the cooling channel.  
  PV format: `$(P):$(R):STATE_RB`

- **Set Status PV (`STATE_SP`)**  
  Enables the user to change the status or mode of the channel.  
  PV format: `$(P):$(R):STATE_SP`

### Possible Values for `STATE_RB` and `STATE_SP`

The status PVs typically represent the operational state of the cooling channel. Possible values may include (depending on your IOC implementation):

- `OFF` – Channel is powered off or inactive
- `ON` – Channel is active and cooling
- `STANDBY` – Channel is in standby mode
- `FAULT` – Channel has detected a fault condition
- `MAINTENANCE` – Channel is in maintenance mode

These values are shown in the status display (`STATE_RB`) and can be selected or set via the combo box widget (`STATE_SP`).

### Additional Macros

- **NAME**: The name of the sensor or channel, displayed in the interface.
- **ZONE**: The zone or area associated with the channel.
- **OPI**: The path to a custom control OPI file for advanced actions.
- **LCID**: Local channel identifier used for control logic.

### Widget Overview

- **Readout**: Displays the current temperature.
- **SetPoint**: Allows entry of a new temperature setpoint.
- **Status**: Shows the current operational state.
- **Set Status**: Provides a combo box to change the channel's state.
- **Custom Control Button**: Opens a custom OPI for advanced control if configured.

### PV Naming Convention

All PVs are constructed using the macro substitutions `$(P)` (prefix) and `$(R)` (record or channel identifier), ensuring the interface can be reused for multiple cooling channels by simply changing the macro values.

---

