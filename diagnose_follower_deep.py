#!/usr/bin/env python3
"""Deep diagnostic of follower motors 1, 2, 6."""

import sys
import time
sys.path.insert(0, "/Users/shraavastibhat/lerobot/src")

import scservo_sdk as scs

PORT = "/dev/cu.usbmodem5AAF2637511"  # Follower arm
BAUDRATE = 1000000

port_handler = scs.PortHandler(PORT)
packet_handler = scs.PacketHandler(0)

port_handler.openPort()
port_handler.setBaudRate(BAUDRATE)

def read_byte(motor_id, address):
    data, result, error = packet_handler.readTxRx(port_handler, motor_id, address, 1)
    return (data[0] if data else None, result, error)

def read_2byte(motor_id, address):
    data, result, error = packet_handler.readTxRx(port_handler, motor_id, address, 2)
    val = data[0] + (data[1] << 8) if data else None
    return (val, result, error)

def write_byte(motor_id, address, value):
    result, error = packet_handler.writeTxRx(port_handler, motor_id, address, 1, [value])
    return (result, error)

motor_names = {1: "F1 shoulder_pan", 2: "F2 shoulder_lift", 6: "F6 gripper"}

print(f"Deep diagnostic of follower motors on {PORT}\n")

for motor_id in [1, 2, 6]:
    name = motor_names[motor_id]
    print(f"=== Motor {motor_id} ({name}) ===")

    # Read various registers
    model, r, e = read_2byte(motor_id, 3)
    print(f"  Model Number: {model}")

    pos, r, e = read_2byte(motor_id, 56)
    print(f"  Present Position: {pos}")

    goal, r, e = read_2byte(motor_id, 42)
    print(f"  Goal Position: {goal}")

    torque, r, e = read_byte(motor_id, 40)
    print(f"  Torque Enable: {torque}")

    lock, r, e = read_byte(motor_id, 55)
    print(f"  Lock: {lock} (1=EPROM locked)")

    status, r, e = read_byte(motor_id, 65)
    print(f"  Status/Error: {status}")

    # Read voltage
    voltage, r, e = read_byte(motor_id, 62)
    if voltage:
        print(f"  Voltage: {voltage/10:.1f}V")

    # Try enabling torque and verify
    print(f"\n  Enabling torque...")
    result, error = write_byte(motor_id, 40, 1)
    print(f"    Write result: {result} (0=success), error: {error}")
    time.sleep(0.1)

    torque_after, r, e = read_byte(motor_id, 40)
    print(f"    Torque after write: {torque_after}")

    if torque_after != 1:
        print(f"    WARNING: Torque did not enable!")

    # Try writing goal position
    target = pos + 200 if pos else 2048
    print(f"\n  Writing goal position {target}...")
    low = target & 0xFF
    high = (target >> 8) & 0xFF
    result, error = packet_handler.writeTxRx(port_handler, motor_id, 42, 2, [low, high])
    print(f"    Write result: {result}, error: {error}")

    time.sleep(0.5)

    goal_after, r, e = read_2byte(motor_id, 42)
    pos_after, r, e = read_2byte(motor_id, 56)
    print(f"    Goal after write: {goal_after}")
    print(f"    Position after: {pos_after}")

    # Disable torque
    write_byte(motor_id, 40, 0)
    print()

port_handler.closePort()
