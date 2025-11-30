import csv
import random

# Postal codes
POSTAL_CODES = [
    ("10001", "New York", "NY", 40.7505, -73.9934),
    ("90210", "Beverly Hills", "CA", 34.0901, -118.4065),
    ("77001", "Houston", "TX", 29.7589, -95.3677),
    ("33101", "Miami", "FL", 25.7617, -80.1918),
    ("85001", "Phoenix", "AZ", 33.4734, -112.0740)
]

# Site name components
FIRST_NOUNS = ["Eagle", "Summit", "Valley", "River", "Mountain", "Forest", "Crystal", "Golden"]
SECOND_NOUNS = ["Creek", "Ridge", "Hill", "Brook", "Grove", "Field", "Point", "Rock"]

data = []
for i in range(1, 51):
    postal_code, city, state, lat, lng = random.choice(POSTAL_CODES)
    site_name = f"{random.choice(FIRST_NOUNS)} {random.choice(SECOND_NOUNS)} Site"
    pollution_class = random.choice(["Industrial", "Federal", "Residential"])
    pollution_type = random.choice(["Nuclear", "Chemical", "Biological"])
    status = random.choice(["Evaluating", "Planned", "In Progress", "Completed"])
    
    # Simple dates
    start_date = "2024-01-01" if status != "Evaluating" else ""
    finish_date = "2025-12-31" if status != "Evaluating" else ""
    
    address = f"{random.randint(100,999)} {random.choice(['Industrial Blvd', 'Factory Rd', 'Chemical Ave'])}"
    
    row = [i, site_name, pollution_class, pollution_type, status, start_date, finish_date, 
           address, city, state, postal_code, "USA", lat, lng]
    data.append(row)

# Write CSV with proper formatting
with open('superfundsites.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['Id', 'SiteName', 'PollutionClass', 'PollutionType', 'RemediationStatus', 
                     'RemediationStart', 'RemediationFinish', 'AddressLine', 'City', 
                     'StateProvince', 'PostalCode', 'Country', 'Latitude', 'Longitude'])
    for row in data:
        formatted_row = []
        for i, value in enumerate(row):
            if i in [0, 12, 13]:  # Id, Latitude, Longitude are numeric
                formatted_row.append(value)
            else:  # All other fields are strings
                formatted_row.append(str(value))
        writer.writerow(formatted_row)

print("Generated 50 superfund sites with SiteName field")
