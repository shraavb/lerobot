#!/usr/bin/env python3
"""Diagnostic script to check motor position reading."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors.motors_bus import Motor, MotorNormMode

PORT = "/dev/cu.usbmodem5AA90244191"

# SO101 follower motor configuration
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

print("\nReading raw positions (no calibration applied)...")
print("Move the joints and watch if values change!\n")

try:
    for i in range(10):
        positions = bus.sync_read("Present_Position", normalize=False)
        print(f"Read {i+1}:")
        for name, pos in positions.items():
            print(f"  {name}: {pos}")
        print()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    bus.disconnect()
    print("Disconnected")
