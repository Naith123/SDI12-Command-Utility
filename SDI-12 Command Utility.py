"""
SDI-12 Serial Command Utility
----------------------------------
Author: Nathan Raj
Created: 2025-03-29
Version: 1.0
License: MIT License

Description:
This script allows users to connect to an SDI-12 sensor via a configurable COM port and send arbitrary 
commands. It includes features such as:
- Selecting or changing the COM port at runtime
- Sending commands manually via text input
- Caching the last N commands for quick resending
- Logging all activity (commands sent, responses received, errors, and configuration changes)
- Creating a new log file for each program session

Requirements:
- Python 3.12.6
- pyserial (`pip install pyserial`)

Usage:
1. Run the script and enter the COM port when prompted.
2. Enter SDI-12 commands manually or use history shortcuts.
3. Type 'history' to see past commands, 'configure' to change the COM port, or 'exit' to quit.

Copyright (C) Nathan Raj, 2025.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial
import time
import collections
import os
from datetime import datetime

# Configuration
DEFAULT_BAUD_RATE = 1200  # SDI-12 typically uses 1200 baud
TIMEOUT = 2  # Response timeout in seconds
MAX_HISTORY = 10  # Number of commands to cache

# Initialize command history
command_history = collections.deque(maxlen=MAX_HISTORY)

# Create log directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log filename based on timestamp
log_filename = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# Store the COM port (set at startup)
current_com_port = None
serial_connection = None

def log_message(message):
    """Write a message to the log file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    
    # Print to console
    print(log_entry)

    # Append to log file
    with open(log_filename, "a") as log_file:
        log_file.write(log_entry + "\n")

def open_serial_port(com_port):
    """Open and return a serial connection."""
    global serial_connection, current_com_port

    # Close any existing connection before opening a new one
    if serial_connection and serial_connection.is_open:
        serial_connection.close()
        log_message(f"Closed previous connection on {current_com_port}")

    try:
        serial_connection = serial.Serial(com_port, DEFAULT_BAUD_RATE, timeout=TIMEOUT)
        current_com_port = com_port
        log_message(f"Connected to {com_port} at {DEFAULT_BAUD_RATE} baud.")
    except serial.SerialException as e:
        log_message(f"Error opening serial port {com_port}: {e}")
        serial_connection = None

def send_command(command):
    """Send an SDI-12 command and read response."""
    if not serial_connection or not serial_connection.is_open:
        log_message("Serial port is not open. Use 'configure' to set a COM port.")
        return

    # Ensure command ends with a carriage return
    command = command.strip() + "\r"
    
    try:
        # Send command
        serial_connection.write(command.encode('ascii'))
        log_message(f"Sent command: {command.strip()}")

        time.sleep(0.5)  # Small delay for sensor processing

        # Read response
        response = serial_connection.read_until(b'\r').decode('ascii').strip()
        log_message(f"Response: {response}")

        # Cache command
        if command not in command_history:
            command_history.append(command.strip())

    except Exception as e:
        log_message(f"Error communicating with sensor: {e}")

def list_command_history():
    """Display cached command history."""
    if not command_history:
        log_message("No commands in history.")
        return
    
    log_message("Command History Accessed:")
    for i, cmd in enumerate(command_history):
        log_message(f"{i+1}: {cmd}")

def configure_port():
    """Allows the user to set or change the COM port."""
    global current_com_port

    new_com_port = input("Enter COM port (e.g., COM3, /dev/ttyUSB0): ").strip()
    
    if new_com_port:
        log_message(f"Setting COM port to {new_com_port}...")
        open_serial_port(new_com_port)

def main():
    global current_com_port

    # Initial COM port setup
    configure_port()

    if not serial_connection:
        log_message("No valid COM port set. Exiting.")
        return

    try:
        while True:
            print("\nEnter an SDI-12 command, type 'history' to view past commands, 'configure' to change COM port, or 'exit' to quit.")
            user_input = input("Command: ").strip()

            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "history":
                list_command_history()
            elif user_input.lower() == "configure":
                configure_port()
            elif user_input.isdigit() and 1 <= int(user_input) <= len(command_history):
                # Send a command from history
                command_index = int(user_input) - 1
                send_command(command_history[command_index])
            else:
                send_command(user_input)

    finally:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
            log_message("Serial connection closed.")

if __name__ == "__main__":
    log_message("Program started.")
    main()
    log_message("Program exited.")
