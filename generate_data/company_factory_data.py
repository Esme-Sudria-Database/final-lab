from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd

fake = Faker()

# Initialize empty lists for each table
companies = []
factories = []
production_lines = []
products = []
product_parts = []
production_line_reports = []
product_market = []

OUTPUT_FOLDER = "generate_data/output"
COMPANY_NUMBER = 8
PRODUCT_NUMBER = 100
PRODUCT_PARTS_NUMBER = 5
FACTORY_NUMBER_MIN = 2
FACTORY_NUMBER_MAX = 6
PRODUCTION_LINE_NUMBER_MIN = 2
PRODUCTION_LINE_NUMBER_MAX = 5
PRODUCTION_LINE_REPORT_NUMBER = 365

# Add new constant for SQL file
OUTPUT_SQL_FILE = "generate_data/output/factories.sql.dump"

# Add sensor types constant
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

# Generate Companies (8 companies)
for company_id in range(1, COMPANY_NUMBER + 1):
    companies.append({
        'company_id': company_id,
        'company_name': fake.company(),
        'industry': random.choice([
            "Manufacturing", "Automotive", "Electronics",
            "Food Processing", "Pharmaceuticals", "Chemical"
        ]),
        'nationality': fake.country(),
        'number_of_employees': random.randint(1000, 50000)
    })

# Generate Products (10 products)
for product_id in range(1, PRODUCT_NUMBER + 1):
    products.append({
        'id': product_id,
        'name': fake.catch_phrase()
    })

    # Generate Product Parts (1-5 parts per product)
    num_parts = random.randint(1, PRODUCT_PARTS_NUMBER)
    for part_id in range(1, num_parts + 1):
        product_parts.append({
            'id': len(product_parts) + 1,
            'name': f"Part {part_id} - {random.choice(['screw', 'bolt', 'nut', 'washer', 'spring', 'gear', 'bearing', 'shaft', 'gasket', 'valve'])}",
            'product_id': product_id
        })

# Generate Factories and Production Lines
factory_id_counter = 1
production_line_id_counter = 1

for company in companies:
    # Each company has 3-5 factories
    num_factories = random.randint(FACTORY_NUMBER_MIN, FACTORY_NUMBER_MAX)

    for _ in range(num_factories):
        city = fake.city()
        factories.append({
            'factory_id': factory_id_counter,
            'factory_name': f"Factory {factory_id_counter} - {city}",
            'city': city,
            'country': fake.country(),
            'company_id': company['company_id']
        })

        # Each factory has 2-4 production lines
        num_production_lines = random.randint(PRODUCTION_LINE_NUMBER_MIN, PRODUCTION_LINE_NUMBER_MAX)
        for line_num in range(num_production_lines):
            line_id = f"LINE-{factory_id_counter}-{line_num + 1}"
            production_lines.append({
                'line_id': line_id,
                'line_name': f"Production Line {line_num + 1}",
                'line_type': random.choice(["Assembly", "Packaging", "Testing", "Processing"]),
                'factory_id': factory_id_counter,
                'product_part': random.choice(product_parts)['id']
            })

            # Generate production line reports for the last year
            start_date = datetime.now() - timedelta(days=365)
            for day in range(365):
                current_date = start_date + timedelta(days=day)
                for hour in range(24):
                    production_line_reports.append({
                        'id': len(production_line_reports) + 1,
                        'production_line_id': production_line_id_counter,
                        'production_rate': random.uniform(0.6, 1.0),
                        'date_time': current_date + timedelta(hours=hour)
                    })

            production_line_id_counter += 1
        factory_id_counter += 1

# Generate Product Market data (prices for the last 30 days)
start_date = datetime.now() - timedelta(days=365)
for product in products:
    base_price = random.uniform(100, 1000)
    for day in range(365):
        current_date = start_date + timedelta(days=day)
        # Add some random variation to the price
        daily_price = base_price * random.uniform(0.9, 1.1)
        product_market.append({
            'id': len(product_market) + 1,
            'product_id': product['id'],
            'price': round(daily_price, 2),
            'day': current_date.date().strftime('%Y-%m-%d')
        })

# Convert to DataFrames
df_companies = pd.DataFrame(companies)
df_factories = pd.DataFrame(factories)
df_production_lines = pd.DataFrame(production_lines)
df_products = pd.DataFrame(products)
df_product_parts = pd.DataFrame(product_parts)
df_production_line_reports = pd.DataFrame(production_line_reports)
df_product_market = pd.DataFrame(product_market)

# Replace the CSV export section with SQL generation
def generate_sql_insert(table_name, df):
    insert_statements = []

    # Create table schema
    columns = df.columns.tolist()
    schema = {
        'companies': {
            'company_id': 'INTEGER PRIMARY KEY',
            'company_name': 'VARCHAR(255)',
            'industry': 'VARCHAR(100)',
            'nationality': 'VARCHAR(255)',
            'number_of_employees': 'INTEGER'
        },
        'factories': {
            'factory_id': 'INTEGER PRIMARY KEY',
            'factory_name': 'VARCHAR(255)',
            'city': 'VARCHAR(255)',
            'country': 'VARCHAR(255)',
            'company_id': 'INTEGER'
        },
        'production_lines': {
            'line_id': 'VARCHAR(50) PRIMARY KEY',
            'line_name': 'VARCHAR(255)',
            'line_type': 'VARCHAR(100)',
            'factory_id': 'INTEGER',
            'product_part': 'INTEGER'
        },
        'products': {
            'id': 'INTEGER PRIMARY KEY',
            'name': 'VARCHAR(255)'
        },
        'product_parts': {
            'id': 'INTEGER PRIMARY KEY',
            'name': 'VARCHAR(255)',
            'product_id': 'INTEGER'
        },
        'production_line_reports': {
            'id': 'INTEGER PRIMARY KEY',
            'production_line_id': 'INTEGER',
            'production_rate': 'FLOAT',
            'date_time': 'TIMESTAMP'
        },
        'product_market': {
            'id': 'INTEGER PRIMARY KEY',
            'product_id': 'INTEGER',
            'price': 'DECIMAL(10,2)',
            'day': 'DATE'
        }
    }

    # Create table
    columns_def = ', '.join([f"{col} {schema[table_name][col]}" for col in schema[table_name].keys()])
    create_table = f"DROP TABLE IF EXISTS {table_name};\n"
    create_table += f"CREATE TABLE {table_name} ({columns_def});\n"
    insert_statements.append(create_table)

    # Generate bulk insert statements
    batch_size = 1000  # Adjust based on your needs
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]
        values_list = []

        for _, row in batch_df.iterrows():
            row_values = []
            for col in df.columns:
                val = row[col]
                if pd.isna(val):
                    row_values.append('NULL')
                elif isinstance(val, str):
                    row_values.append(f"'{val.replace('\'', '\'\'')}'")
                elif isinstance(val, (datetime, pd.Timestamp)):
                    row_values.append(f"'{val}'")
                else:
                    row_values.append(str(val))
            values_list.append(f"({', '.join(row_values)})")

        insert = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES\n"
        insert += ',\n'.join(values_list) + ";"
        insert_statements.append(insert)

    return '\n'.join(insert_statements)

# Add these helper functions at the bottom of the file, before the main execution
def generate_company_data():
    return pd.DataFrame(companies)

def generate_factory_data():
    return pd.DataFrame(factories)

# Wrap the main execution in if __name__ == "__main__" to prevent it from running when imported
if __name__ == "__main__":
    # Write to SQL file
    with open(OUTPUT_SQL_FILE, 'w', encoding='utf-8') as f:
        f.write('-- Database initialization script\n\n')
        f.write('BEGIN;\n\n')  # Start transaction

        # Generate INSERT statements for each table
        tables = {
            'companies': df_companies,
            'factories': df_factories,
            'production_lines': df_production_lines,
            'products': df_products,
            'product_parts': df_product_parts,
            'production_line_reports': df_production_line_reports,
            'product_market': df_product_market
        }

        for table_name, df in tables.items():
            f.write(f"\n-- Table: {table_name}\n")
            f.write(generate_sql_insert(table_name, df))
            f.write('\n')

        f.write('\nCOMMIT;\n')  # End transaction

    print("Data generation complete! SQL file has been generated.")
