#!/usr/bin/env python3
"""Check voltage on both arms."""

import sys
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

LEADER_PORT = "/dev/cu.usbmodem5AA90244191"
FOLLOWER_PORT = "/dev/cu.usbmodem5AAF2637511"

motor_names = {1: "shoulder_pan", 2: "shoulder_lift", 3: "elbow_flex",
               4: "wrist_flex", 5: "wrist_roll", 6: "gripper"}

def check_arm(port, arm_name):
    port_handler = scs.PortHandler(port)
    packet_handler = scs.PacketHandler(0)

    if not port_handler.openPort():
        print(f"  Could not open {port}")
        return

    port_handler.setBaudRate(1000000)

    print(f"\n=== {arm_name} ({port}) ===")
    for motor_id in [1, 2, 3, 4, 5, 6]:
        data, result, _ = packet_handler.readTxRx(port_handler, motor_id, 62, 1)
        if result == scs.COMM_SUCCESS and data:
            voltage = data[0] / 10.0
            status = "LOW!" if voltage < 6.0 else "OK"
            print(f"  Motor {motor_id} ({motor_names[motor_id]}): {voltage:.1f}V  {status}")
        else:
            print(f"  Motor {motor_id}: No response")

    port_handler.closePort()

check_arm(LEADER_PORT, "LEADER ARM")
check_arm(FOLLOWER_PORT, "FOLLOWER ARM")

print("\n" + "="*50)
print("Expected: 7.4V-12V for motors to move")
print("5V = USB power only (communication works, motors won't move)")
