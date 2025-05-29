import re
from datetime import datetime

# Symbol Table
sensors = {}
zones = set()
env_vars = {"RAINFALL_FORECAST": None}
schedules = []
intermediate_code = []

# Helpers
def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, '%I:%M %p')
        return True
    except ValueError:
        return False

# Parser & Semantic Analyzer
def parse_sisl_code(lines):
    for line in lines:
        line = line.strip()
        if line.startswith("DECLARE"):
            parts = line.split()
            sensor_type = parts[1]
            zone = parts[2]
            sensors[zone] = sensor_type
            print(f"Declared {sensor_type} in zone {zone}")

        elif line.startswith("GET"):
            var = line.split()[1]
            if var not in env_vars:
                env_vars[var] = None
            print(f"Fetching {var}")

        elif line.startswith("ZONE"):
            zone_name = line.split()[1]
            zones.add(zone_name)
            print(f"Zone defined: {zone_name}")

        elif line.startswith("IF"):
            match = re.match(r"IF (\w+)_SENSOR (\w+) < (\d+) THEN WATER (\w+) FOR (\d+) MINUTES", line)
            if match:
                sensor_type, zone, threshold, water_zone, duration = match.groups()
                threshold, duration = int(threshold), int(duration)
                
                # Semantic checks
                if zone not in sensors or sensor_type not in sensors[zone]:
                    raise Exception(f"Sensor {sensor_type} not declared in zone {zone}.")
                if water_zone not in zones:
                    raise Exception(f"Irrigation zone {water_zone} not declared.")
                if duration <= 0:
                    raise Exception("Watering duration must be a positive integer.")

                # Intermediate Code
                intermediate_code.append(f"READ_SENSOR {sensor_type}, {zone}")
                intermediate_code.append(f"IF_LESS_THAN RESULT, {threshold} GOTO WATER_{water_zone}")
                intermediate_code.append(f"LABEL WATER_{water_zone}")
                intermediate_code.append(f"ACTIVATE_VALVE {water_zone}, {duration * 60}_SECONDS")
                intermediate_code.append(f"DEACTIVATE_VALVE {water_zone}")

                print(f"Conditionally watering {water_zone} if {sensor_type} < {threshold}")

        elif line.startswith("SCHEDULE"):
            match = re.match(r"SCHEDULE WATER (\w+) AT ([0-9]{2}:[0-9]{2} [AP]M) DAILY", line)
            if match:
                water_zone, time_str = match.groups()
                if water_zone not in zones:
                    raise Exception(f"Zone {water_zone} not declared.")
                if not is_valid_time(time_str):
                    raise Exception(f"Invalid time format: {time_str}")

                schedules.append((water_zone, time_str))
                intermediate_code.append(f"SCHEDULE_VALVE {water_zone}, {time_str}")
                print(f"Scheduled daily watering for {water_zone} at {time_str}")
        else:
            if line:
                print(f"Unknown command: {line}")

# Example Input
sisl_code = """
DECLARE SOIL_MOISTURE_SENSOR ZoneA
DECLARE TEMPERATURE_SENSOR ZoneB
GET RAINFALL_FORECAST
ZONE ZoneA_Field

IF SOIL_MOISTURE_SENSOR ZoneA < 30 THEN WATER ZoneA_Field FOR 15 MINUTES
SCHEDULE WATER ZoneA_Field AT 06:00 AM DAILY
"""

# Main Driver
def main():
    lines = sisl_code.strip().split('\n')
    parse_sisl_code(lines)

    print("\n--- Symbol Table ---")
    print("Sensors:", sensors)
    print("Zones:", zones)
    print("Env Vars:", env_vars)
    print("Schedules:", schedules)

    print("\n--- Intermediate Code ---")
    for instruction in intermediate_code:
        print(instruction)

if __name__ == "__main__":
    main()


