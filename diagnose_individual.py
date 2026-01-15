#!/usr/bin/env python3
"""Diagnostic script to check individual motor reads and other registers."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors.motors_bus import Motor, MotorNormMode

PORT = "/dev/cu.usbmodem5AA90244191"

motors = {
    "shoulder_pan": Motor(1, "sts3215", MotorNormMode.RANGE_M100_100),
    "shoulder_lift": Motor(2, "sts3215", MotorNormMode.RANGE_M100_100),
    "elbow_flex": Motor(3, "sts3215", MotorNormMode.RANGE_M100_100),
    "wrist_flex": Motor(4, "sts3215", MotorNormMode.RANGE_M100_100),
    "wrist_roll": Motor(5, "sts3215", MotorNormMode.RANGE_M100_100),
    "gripper": Motor(6, "sts3215", MotorNormMode.RANGE_0_100),
}

print(f"Connecting to motors on {PORT}...")
bus = FeetechMotorsBus(PORT, motors)
bus.connect()

print("\n--- Reading various registers ---\n")

try:
    # Read ID (should return the motor ID)
    print("Motor IDs:")
    for name in motors:
        val = bus.read("ID", name, normalize=False)
        print(f"  {name}: {val}")

    # Read Model_Number
    print("\nModel Numbers:")
    for name in motors:
        val = bus.read("Model_Number", name, normalize=False)
        print(f"  {name}: {val}")

    # Read Present_Position individually
    print("\nPresent_Position (individual reads):")
    for name in motors:
        val = bus.read("Present_Position", name, normalize=False)
        print(f"  {name}: {val}")

    # Read Torque_Enable
    print("\nTorque_Enable (0=disabled/free, 1=enabled/locked):")
    for name in motors:
        val = bus.read("Torque_Enable", name, normalize=False)
        print(f"  {name}: {val}")

    # Read Present_Load/Current
    print("\nPresent_Load:")
    for name in motors:
        try:
            val = bus.read("Present_Load", name, normalize=False)
            print(f"  {name}: {val}")
        except Exception as e:
            print(f"  {name}: Error - {e}")

    print("\n--- Moving shoulder_pan and reading again ---")
    print("Move the SHOULDER (base) joint now!")
    time.sleep(3)

    print("\nPresent_Position after moving:")
    for name in motors:
        val = bus.read("Present_Position", name, normalize=False)
        print(f"  {name}: {val}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    bus.disconnect()
    print("\nDisconnected")
