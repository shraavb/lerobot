"""
Test that mimics the exact teleoperate flow to diagnose the connection error.
"""
from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so101_leader import SO101Leader, SO101LeaderConfig
import time

FOLLOWER_PORT = "/dev/cu.usbmodem5AAF2637511"
LEADER_PORT = "/dev/cu.usbmodem5AA90244191"

print("=" * 60)
print("Mimicking exact teleoperate flow...")
print("=" * 60)

# Create configs exactly as teleoperate does
follower_config = SO101FollowerConfig(
    port=FOLLOWER_PORT,
    id="my_awesome_follower_arm",
)

leader_config = SO101LeaderConfig(
    port=LEADER_PORT,
    id="my_awesome_leader_arm",
)

print("\n1. Creating robot and teleoperator instances...")
robot = SO101Follower(follower_config)
teleop = SO101Leader(leader_config)

print("\n2. Connecting teleoperator (leader)...")
teleop.connect()
print("   Leader connected!")

print("\n3. Connecting robot (follower)...")
robot.connect()
print("   Follower connected!")

print("\n4. Starting teleoperation loop test (20 iterations at 60fps)...")
try:
    for i in range(20):
        loop_start = time.perf_counter()

        # Get robot observation (this is where the error occurs)
        obs = robot.get_observation()

        # Get teleop action
        action = teleop.get_action()

        # Send action to robot
        robot.send_action(action)

        dt_ms = (time.perf_counter() - loop_start) * 1000
        print(f"   Iteration {i+1}: OK ({dt_ms:.1f}ms)")

        # Sleep to maintain ~60fps
        time.sleep(max(0, 1/60 - (time.perf_counter() - loop_start)))

    print("\n   All iterations successful!")

except Exception as e:
    print(f"\n   FAILED: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n5. Disconnecting...")
    try:
        teleop.disconnect()
        print("   Leader disconnected")
    except:
        pass
    try:
        robot.disconnect()
        print("   Follower disconnected")
    except:
        pass

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
