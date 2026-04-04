# unimot-opi
unimotor opi unified view of motors

# unimot-opi
unimotor opi unified view of motors

## PV Interface for `mot_channel.bob`

The `mot_channel.bob` OPI provides a unified interface for monitoring and controlling motor channels. It uses the following Process Variables (PVs), parameterized via macros for flexibility:

- **Position Readback PV (`RBV`)**  
  Displays the current position of the motor.  
  PV format: `$(P):$(R):RBV`

- **Position Setpoint PV (`VAL_SP`)**  
  Shows the setpoint value for the motor position.  
  PV format: `$(P):$(R):VAL_SP`

- **Relative Move PV (`RVAL`)**  
  Allows entry of a relative move value for the motor.  
  PV format: `$(P):$(R):RVAL`

- **Absolute Move PV (`VAL`)**  
  Allows entry of an absolute move value for the motor.  
  PV format: `$(P):$(R):VAL`

- **Position Readback in mm (`MM_RBV`)**  
  Displays the position in millimeters if enabled.  
  PV format: `$(P):$(R):MM_RBV`

- **Absolute Move in mm (`VAL_MM`)**  
  Allows entry of an absolute move value in millimeters if enabled.  
  PV format: `$(P):$(R):VAL_MM`

- **Relative Move in mm (`RVAL_MM`)**  
  Allows entry of a relative move value in millimeters if enabled.  
  PV format: `$(P):$(R):RVAL_MM`

- **Setpoint in mm (`VAL_MM_SP`)**  
  Shows the setpoint value in millimeters if enabled.  
  PV format: `$(P):$(R):VAL_MM_SP`

- **Motor Status PVs (`MSTA.B2`, `MSTA.BA`, `MSTA.B9`, `MSTA.BD`)**  
  Indicate various motor status bits (enabled, alarm, stop, direction, etc.).  
  PV formats:  
    - `$(P):$(R):MSTA.B2` (enabled)  
    - `$(P):$(R):MSTA.BA` (alarm)  
    - `$(P):$(R):MSTA.B9` (stop)  
    - `$(P):$(R):MSTA.BD` (direction)

- **Motor Command PV (`CMD`)**  
  Used for sending commands such as HOME, JOG FORWARD, JOG REVERSE.  
  PV format: `$(P):$(R):CMD`

- **Motor Action PV (`ACTX_SP`)**  
  Used for actions such as STOP.  
  PV format: `$(P):$(R):ACTX_SP`

- **Motor Message PV (`MSGS`)**  
  Used for connect/disconnect actions.  
  PV format: `$(P):$(R):MSGS`

- **Progress Bar PV (`DRBV_RB`)**  
  Displays the position as a progress bar.  
  PV format: `$(P):$(R):DRBV_RB`

### Possible Values for Motor States

Motor states are typically represented by the status PVs and command PVs. Possible values and actions include:

- **Enable/Disable**:  
  - `MSGS` PV: Write `START` to connect, `STOP` to disconnect.
- **Commands**:  
  - `CMD` PV: Write `3` for HOME, `4` for JOG FORWARD, `5` for JOG REVERSE.
- **Action**:  
  - `ACTX_SP` PV: Write `2` for STOP.
- **Status Bits**:  
  - `MSTA.B2`: Motor enabled (LED indicator)
  - `MSTA.BA`: Alarm status (LED indicator)
  - `MSTA.B9`: Stop status (LED indicator)
  - `MSTA.BD`: Direction status (LED indicator)

### Additional Macros

- **NAME**: The name of the motor or channel, displayed in the interface.
- **ZONE**: The zone or area associated with the motor.
- **TYPE**: The type of motor.
- **OPI**: The path to a custom control OPI file for advanced actions.

### Widget Overview

- **Label**: Shows the motor name and zone.
- **Text Update**: Displays position and setpoint values.
- **Text Entry**: Allows entry of relative and absolute move values.
- **LEDs**: Indicate motor status bits.
- **Action Buttons**: For connect/disconnect, stop, home, jog commands.
- **Progress Bar**: Shows position as a linear meter.
- **Custom Control Button**: Opens a custom OPI for advanced control if configured.

### PV Naming Convention

All PVs are constructed using macro substitutions `$(P)` (prefix) and `$(R)` (record or channel identifier), ensuring the interface can be reused for multiple motors by simply changing the macro values.

---

