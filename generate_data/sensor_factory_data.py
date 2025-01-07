import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from company_factory_data import generate_company_data, generate_factory_data
import os

# Constants for sensor types and their characteristics
SENSOR_TYPES = {
    'pressure': {
        'unit': 'bar',
        'min_value': 0,
        'max_value': 100,
        'precision': 2
    },
    'temperature': {
        'unit': '°C',
        'min_value': -20,
        'max_value': 150,
        'precision': 1
    },
    'speed': {
        'unit': 'rpm',
        'min_value': 0,
        'max_value': 5000,
        'precision': 0
    },
    'lightness': {
        'unit': 'lux',
        'min_value': 0,
        'max_value': 1000,
        'precision': 0
    },
    'air_quality': {
        'unit': 'AQI',
        'min_value': 0,
        'max_value': 500,
        'precision': 0
    }
}

def generate_sensor_id():
    return f"SEN-{random.randint(10000, 99999)}"

def generate_sensor_metadata(company, factory, production_line):
    metadata = {
        "installation_date": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
        "manufacturer": random.choice(["Siemens", "ABB", "Honeywell", "Schneider Electric", "Emerson"]),
        "model": f"Model-{random.randint(1000, 9999)}",
        "firmware_version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "calibration_date": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat(),
        "maintenance_interval": f"{random.randint(30, 365)} days",
        "company_id": company["company_id"],
        "factory_id": factory["factory_id"],
        "production_line_id": production_line["line_id"]
    }
    return metadata

def generate_sensor_data():
    # Get company and factory data from the other script
    companies_df = generate_company_data()
    factories_df = generate_factory_data()

    sensors = []

    for _, factory in factories_df.iterrows():
        # Convert numpy/pandas types to native Python types
        factory = factory.to_dict()
        company = companies_df[companies_df['company_id'] == factory['company_id']].iloc[0].to_dict()

        # Generate 2-5 production lines per factory
        num_production_lines = random.randint(2, 5)
        for line_num in range(1, num_production_lines + 1):
            production_line = {
                "line_id": f"LINE-{factory['factory_id']}-{line_num}",
                "line_name": f"Production Line {line_num}",
                "line_type": random.choice(["Assembly", "Packaging", "Testing", "Processing"])
            }

            # Generate 1-3 sensors of each type for each production line
            for sensor_type, characteristics in SENSOR_TYPES.items():
                num_sensors = random.randint(1, 3)
                for _ in range(num_sensors):
                    sensor = {
                        "sensor_id": generate_sensor_id(),
                        "sensor_type": sensor_type,
                        "status": random.choice(["active", "active", "active", "maintenance", "error"]),

                        # Company and factory information
                        "company": {
                            "company_id": str(company['company_id']),  # Convert to string
                            "company_name": company['company_name'],
                            "industry": company['industry']
                        },
                        "factory": {
                            "factory_id": str(factory['factory_id']),  # Convert to string
                            "factory_name": factory['factory_name'],
                            "location": {
                                "country": factory['country'],
                                "city": factory['city']
                            }
                        },
                        "production_line": production_line,

                        # Sensor specific information
                        "specifications": {
                            "measurement_unit": characteristics['unit'],
                            "measurement_range": {
                                "min": float(characteristics['min_value']),  # Convert to float
                                "max": float(characteristics['max_value'])   # Convert to float
                            },
                            "precision": int(characteristics['precision'])   # Convert to int
                        },

                        # Current reading
                        "current_reading": {
                            "value": float(round(random.uniform(  # Convert to float
                                characteristics['min_value'],
                                characteristics['max_value']
                            ), characteristics['precision'])),
                            "timestamp": datetime.now().isoformat()
                        },

                        # Metadata
                        "metadata": generate_sensor_metadata(company, factory, production_line)
                    }
                    sensors.append(sensor)

    return sensors

def main():
    print("Generating sensor data...")
    sensors = generate_sensor_data()

    output_file = 'output/sensors.json'

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write to JSON file

    with open(output_file, 'w') as f:
        json.dump(sensors, f, indent=2)

    print(f"Generated {len(sensors)} sensors data")
    print(f"Data written to {output_file}")

if __name__ == "__main__":
    main()
