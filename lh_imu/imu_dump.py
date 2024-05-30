import subprocess
import re
from datetime import datetime

DONGLE_SERIAL = "8DCB2863B3-DYX" # Dongle Serial
EXE_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\SteamVR\tools\lighthouse\bin\win64\lighthouse_console.exe"

def execute_commands(commands, exe_path):
    process = subprocess.Popen(
        exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
    )
    
    for command in commands:
        process.stdin.write(command + '\n')
        process.stdin.flush()
    
    process.stdin.close()
    return process

def parse_data(line):
    pattern = re.compile(r"gyro ([\d\.\+\-]+) ([\d\.\+\-]+) ([\d\.\+\-]+) accel ([\d\.\+\-]+) ([\d\.\+\-]+) ([\d\.\+\-]+)")
    match = pattern.search(line)
    
    if match:
        return tuple(map(float, match.groups()))
    else:
        return None

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def main():
    commands = [
        f"serial {DONGLE_SERIAL}",
        "dump",
        "imu"
    ]
    
    try:
        process = execute_commands(commands, EXE_PATH)
        gyro_data = []
        accel_data = []

        while True:
            line = process.stdout.readline()
            if not line:
                break

            data = parse_data(line)
            if data:
                timestamp = get_timestamp()
                gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = data
                gyro_data.append([gyro_x, gyro_y, gyro_z])
                accel_data.append([accel_x, accel_y, accel_z])
                print(f"{timestamp} | Gyro (°/s): x={gyro_x}, y={gyro_y}, z={gyro_z} | Accel (m/s²): x={accel_x}, y={accel_y}, z={accel_z}")

        process.communicate()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if process.returncode is None:
            process.kill()

if __name__ == "__main__":
    main()
