# univac-opi Unified VAC interface

## PV Interface for `vac_channel.bob`

The `vac_channel.bob` OPI provides a unified interface for monitoring and controlling vacuum channels. It uses the following Process Variables (PVs), parameterized via macros for flexibility:

- **Pressure Readback PV (`PRES_RB`)**  
  Displays the current pressure readout for the vacuum channel.  
  PV format: `$(P):$(R):PRES_RB`

- **Sensor Type PV (`TYPE`)**  
  Indicates the type of vacuum sensor (e.g., ion pump, CCG, PIG).  
  PV format: `loc://$(P):$(R)_TYPE<type>($(TYPE))`  
  The widget displays different symbols depending on the sensor type.

- **Sensor Name (`NAME`)**  
  The name of the sensor or channel, displayed in the interface.  
  Macro: `$(NAME)`

- **Zone (`ZONE`)**  
  The zone or area associated with the vacuum channel.  
  Macro: `$(ZONE)`

- **Custom Control OPI (`OPI`)**  
  Path to a custom control OPI file for advanced actions.  
  Macro: `$(OPI)`


### Widget Overview

- **Pressure Readout**: Shows the current pressure value with three decimal places.
- **Sensor Type Symbol**: Displays an icon representing the sensor type (ion pump, CCG, PIG, or fallback gas symbol).
- **Sensor Name Label**: Shows the name of the sensor.
- **Zone Label**: Displays the zone information.
- **Custom Control Button**: Opens a custom OPI for advanced control if configured and enabled.
- **Graph Action**: Clicking the sensor type symbol opens a historical graph display (`histoval.bob`).

### PV Naming Convention

All PVs are constructed using macro substitutions `$(P)` (prefix), `$(R)` (record or channel identifier), and other macros, ensuring the interface can be reused for multiple vacuum channels by simply changing the macro values.

