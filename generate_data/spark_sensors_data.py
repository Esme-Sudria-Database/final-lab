from datetime import datetime, timedelta
import random

def generate_sensor_readings():
    # Define 5 different sensor IDs
    sensor_ids = ["SEN-50442", "SEN-61064", "SEN-73291", "SEN-84532", "SEN-95124"]

    # Sensor specifications based on sensor types
    sensor_specs = {
        "SEN-50442": {"type": "pressure", "min": 0.0, "max": 100.0, "precision": 2},
        "SEN-61064": {"type": "temperature", "min": -20.0, "max": 150.0, "precision": 1},
        "SEN-73291": {"type": "humidity", "min": 0.0, "max": 100.0, "precision": 1},
        "SEN-84532": {"type": "vibration", "min": 0.0, "max": 50.0, "precision": 2},
        "SEN-95124": {"type": "flow_rate", "min": 0.0, "max": 200.0, "precision": 1}
    }

    # Initialize result list
    readings = []

    # Set time period
    start_time = datetime.now()
    end_time = start_time + timedelta(days=30)

    # Generate readings for each sensor
    for sensor_id in sensor_ids:
        current_time = start_time
        specs = sensor_specs[sensor_id]

        while current_time < end_time:
            # Generate reading
            value = round(random.uniform(specs["min"], specs["max"]), specs["precision"])

            reading = {
                "sensor_id": sensor_id,
                "sensor_type": specs["type"],
                "value": value,
                "timestamp": current_time.isoformat()
            }
            readings.append(reading)

            # Add random time interval (10-30 seconds)
            interval = random.uniform(10, 30)
            current_time += timedelta(seconds=interval)

    # Write readings to SQL file
    output_file = 'output/sensors.sql.dump'
    batch_size = 1000  # Number of records per INSERT statement

    with open(output_file, 'w') as f:
        # Write CREATE TABLE statement
        f.write("""CREATE TABLE IF NOT EXISTS sensor_readings (
            sensor_id VARCHAR(20),
            sensor_type VARCHAR(20),
            value FLOAT,
            timestamp TIMESTAMP
        );\n\n""")

        # Write batch INSERT statements
        for i in range(0, len(readings), batch_size):
            batch = readings[i:i + batch_size]
            values_strings = []

            for reading in batch:
                values_strings.append(
                    f"('{reading['sensor_id']}', "
                    f"'{reading['sensor_type']}', "
                    f"{reading['value']}, "
                    f"'{reading['timestamp']}')"
                )

            sql = f"""INSERT INTO sensor_readings
                (sensor_id, sensor_type, value, timestamp)
                VALUES {','.join(values_strings)};\n"""
            f.write(sql)

    print(f"SQL statements written to {output_file}")
    return readings

if __name__ == "__main__":
    generate_sensor_readings()
