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

# Generate Companies (8 companies)
for company_id in range(1, 9):
    companies.append({
        'id': company_id,
        'name': fake.company(),
        'nationality': fake.country(),
        'number_of_employees': random.randint(1000, 50000)
    })

# Generate Products (10 products)
for product_id in range(1, 11):
    products.append({
        'id': product_id,
        'name': fake.catch_phrase()
    })

    # Generate Product Parts (1-5 parts per product)
    num_parts = random.randint(1, 5)
    for part_id in range(1, num_parts + 1):
        product_parts.append({
            'id': len(product_parts) + 1,
            'name': f"Part {part_id} - {fake.word()}",
            'product_id': product_id
        })

# Generate Factories and Production Lines
factory_id_counter = 1
production_line_id_counter = 1

for company in companies:
    # Each company has 3-5 factories
    num_factories = random.randint(3, 5)

    for _ in range(num_factories):
        factories.append({
            'id': factory_id_counter,
            'name': f"Factory {factory_id_counter} - {fake.city()}",
            'location': fake.city(),
            'company_id': company['id']
        })

        # Each factory has 2-4 production lines
        num_production_lines = random.randint(2, 4)
        for _ in range(num_production_lines):
            # Randomly assign a product part to the production line
            random_part = random.choice(product_parts)

            production_lines.append({
                'id': production_line_id_counter,
                'name': f"Line {production_line_id_counter}",
                'factory_id': factory_id_counter,
                'product_part': random_part['id']
            })

            # Generate production line reports for the last 30 days
            start_date = datetime.now() - timedelta(days=30)
            for day in range(30):
                current_date = start_date + timedelta(days=day)
                production_line_reports.append({
                    'id': len(production_line_reports) + 1,
                    'production_line_id': production_line_id_counter,
                    'production_rate': random.uniform(0.6, 1.0),
                    'day': current_date.date()
                })

            production_line_id_counter += 1
        factory_id_counter += 1

# Generate Product Market data (prices for the last 30 days)
start_date = datetime.now() - timedelta(days=30)
for product in products:
    base_price = random.uniform(100, 1000)
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        # Add some random variation to the price
        daily_price = base_price * random.uniform(0.9, 1.1)
        product_market.append({
            'id': len(product_market) + 1,
            'product_id': product['id'],
            'price': round(daily_price, 2),
            'day': current_date.date()
        })

# Convert to DataFrames
df_companies = pd.DataFrame(companies)
df_factories = pd.DataFrame(factories)
df_production_lines = pd.DataFrame(production_lines)
df_products = pd.DataFrame(products)
df_product_parts = pd.DataFrame(product_parts)
df_production_line_reports = pd.DataFrame(production_line_reports)
df_product_market = pd.DataFrame(product_market)

# Save to CSV files
df_companies.to_csv(f'{OUTPUT_FOLDER}/companies.csv', index=False)
df_factories.to_csv(f'{OUTPUT_FOLDER}/factories.csv', index=False)
df_production_lines.to_csv(f'{OUTPUT_FOLDER}/production_lines.csv', index=False)
df_products.to_csv(f'{OUTPUT_FOLDER}/products.csv', index=False)
df_product_parts.to_csv(f'{OUTPUT_FOLDER}/product_parts.csv', index=False)
df_production_line_reports.to_csv(f'{OUTPUT_FOLDER}/production_line_reports.csv', index=False)
df_product_market.to_csv(f'{OUTPUT_FOLDER}/product_market.csv', index=False)

print("Data generation complete! Files have been saved as CSVs.")
