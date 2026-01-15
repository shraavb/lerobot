#!/usr/bin/env python3
"""Diagnose leader arm motors."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

from lerobot.motors.feetech import FeetechMotorsBus

PORT = "/dev/cu.usbmodem5AA90244191"  # Leader arm port

print(f"Scanning leader arm on {PORT}...")
result = FeetechMotorsBus.scan_port(PORT)

print("\nScan results:")
for baudrate, motor_ids in result.items():
    if motor_ids:
        print(f"  Baudrate {baudrate}: Found motor IDs {motor_ids}")

if not any(result.values()):
    print("  No motors found!")
else:
    # Check which motors are missing
    found_ids = []
    for ids in result.values():
        found_ids.extend(ids.keys() if isinstance(ids, dict) else ids)

    expected = [1, 2, 3, 4, 5, 6]
    missing = [i for i in expected if i not in found_ids]
    if missing:
        print(f"\n  WARNING: Missing motor IDs: {missing}")
    else:
        print(f"\n  All 6 motors found!")
