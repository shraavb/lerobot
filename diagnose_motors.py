#!/usr/bin/env python3
"""Diagnostic script to check motor communication."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

from lerobot.motors.feetech import FeetechMotorsBus

PORT = "/dev/cu.usbmodem5AA90244191"

print(f"Scanning port {PORT} for motors...")
print("This may take a moment...\n")

try:
    result = FeetechMotorsBus.scan_port(PORT)
    print("Scan results:")
    for baudrate, motor_ids in result.items():
        if motor_ids:
            print(f"  Baudrate {baudrate}: Found motor IDs {motor_ids}")

    if not any(result.values()):
        print("  No motors found at any baudrate!")
        print("\nPossible issues:")
        print("  1. Wrong port - check if this is the correct USB device")
        print("  2. Power issue - ensure the robot is powered on")
        print("  3. Cable issue - check USB and motor bus connections")
except Exception as e:
    print(f"Error during scan: {e}")
