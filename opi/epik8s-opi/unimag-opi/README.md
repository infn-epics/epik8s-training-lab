# unimag-opi
unified view of Magnets


## PV Interface for `mag_channel.bob`

The `mag_channel.bob` OPI provides a unified interface for monitoring and controlling magnet channels. It uses the following Process Variables (PVs), parameterized via macros for flexibility:

- **Current Readback PV (`CURRENT_RB`)**  
  Displays the current readback value for the magnet channel.  
  PV format: `$(P):$(R):CURRENT_RB`

- **Current Setpoint PV (`CURRENT_SP`)**  
  Allows the user to set the desired current for the magnet channel.  
  PV format: `$(P):$(R):CURRENT_SP`

- **Status PV (`STATE_RB`)**  
  Shows the current status or state of the magnet channel.  
  PV format: `$(P):$(R):STATE_RB`

- **Set Status PV (`STATE_SP`)**  
  Enables the user to change the status or mode of the channel (e.g., via ON, STBY, RESET buttons).  
  PV format: `$(P):$(R):STATE_SP`

### Possible Values for `STATE_RB` and `STATE_SP`

The status PVs represent the operational state of the magnet channel. Possible values include:

- `OFF` – Magnet is powered off or inactive
- `ON` – Magnet is active and powered
- `STANDBY` – Magnet is in standby mode
- `FAULT` – Magnet has detected a fault condition
- `RESET` – Magnet is being reset
- Additional states may be supported depending on IOC implementation

These values are displayed in the status widgets and can be set using the action buttons in the OPI.

### Additional Macros

- **NAME**: The name of the magnet or channel, displayed in the interface.
- **ZONE**: The zone or area associated with the channel.
- **OPI**: The path to a custom control OPI file for advanced actions.

### Widget Overview

- **Readout**: Displays the current value.
- **SetPoint**: Allows entry of a new current setpoint.
- **Status**: Shows the current operational state.
- **Set Status**: Provides buttons to change the channel's state (ON, STBY, RESET).
- **Custom Control Button**: Opens a custom OPI for advanced control if configured.
- **Checkbox**: Used for selection logic in multi-magnet views.

### PV Naming Convention

All PVs are constructed using macro substitutions `$(P)` (prefix) and `$(R)` (record or channel identifier), ensuring the interface can be reused for multiple magnet channels by simply changing the macro values.

---

For more details on the OPI layout and macro usage, refer