import csv
import random

# Simple data
POSTAL_CODES = [
    ("10001", "New York", "NY", 40.7505, -73.9934),
    ("90210", "Beverly Hills", "CA", 34.0901, -118.4065),
    ("77001", "Houston", "TX", 29.7589, -95.3677)
]

data = []
for i in range(1, 51):
    postal_code, city, state, lat, lng = random.choice(POSTAL_CODES)
    pollution_class = random.choice(["Industrial", "Federal", "Residential"])
    pollution_type = random.choice(["Nuclear", "Chemical", "Biological"])
    status = random.choice(["Evaluating", "Planned", "In Progress", "Completed"])
    
    row = [i, pollution_class, pollution_type, status, "2025-01-01", "2025-12-31", 
           f"{random.randint(100,999)} Industrial Ave", city, state, postal_code, "USA", lat, lng]
    data.append(row)

with open('superfundsites.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['Id', 'PollutionClass', 'PollutionType', 'RemediationStatus', 
                     'RemediationStart', 'RemediationFinish', 'AddressLine', 'City', 
                     'StateProvince', 'PostalCode', 'Country', 'Latitude', 'Longitude'])
    for row in data:
        formatted_row = []
        for i, value in enumerate(row):
            if i in [0, 11, 12]:  # Id, Latitude, Longitude
                formatted_row.append(value)
            else:
                formatted_row.append(str(value))
        writer.writerow(formatted_row)

print("Generated 50 superfund sites")
