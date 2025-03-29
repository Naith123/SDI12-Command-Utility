# SDI-12 Serial Command Utility

## Overview
This Python script provides a simple interface to communicate with an **SDI-12 sensor** via a configurable **COM port / device address**. Users can send arbitrary SDI-12 commands and receive responses, with a history feature to easily resend previous commands. All interactions are logged to a file for reference.

## Features
- **Configurable COM Port / Device Address** (Set at startup or changed anytime via a command)
- **Send Arbitrary SDI-12 Commands** via text input
- **Command History** (Easily resend previous commands)
- **Logging** (Creates a new log file for each session, tracking commands, responses, and errors)
- **Cross-Platform Support** (Works on Windows and Linux)

## Requirements
- **Python 3.12.6**
- **`pyserial`** library (Install with `pip install pyserial`)

## Installation
1. Clone or download the repository.
2. Install dependencies with:
   ```sh
   pip install pyserial
   ```
3. Run the script:
   ```sh
   python sdi12_serial.py
   ```

## Usage
### 1. **Set COM Port / Device Address**
At startup, the script will prompt for a serial device:
- **Windows Example**: `COM3`
- **Linux Example**: `/dev/ttyUSB0`

You can also change it later by typing:
```sh
configure
```

### 2. **Send Commands**
Type an SDI-12 command (refer to your sensor’s user guide) and press **Enter**.

### 3. **View Command History**
To see a list of recent commands:
```sh
history
```
To resend a command, enter its number from the list.

### 4. **Exit the Program**
To close the connection and exit, type:
```sh
exit
```

## Logging
Each session creates a new log file in the script's directory (`log_YYYYMMDD_HHMMSS.txt`). Logs include:
- Connection status
- Commands sent
- Responses received
- Errors (if any)
- History accesses

## Troubleshooting
- **Cannot open COM port** → Ensure the correct port is selected and that no other program is using it.
- **No response from the sensor** → Check wiring, power, and sensor settings.
- **Permission denied (Linux)** → Try running with:
  ```sh
  sudo python sdi12_serial.py
  ```

## License
This project is licensed under the **MIT License**.

## Author
[Nathan Raj]  
[https://github.com/Naith123/]

