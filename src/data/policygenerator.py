"""
Policy Data Generator
Generates 50 policy records based on the Policy table definition
"""
import csv
import random
from datetime import datetime, timedelta

# Postal codes data from data_definitions.md
POSTAL_CODES = [
    ("10001", "New York", "NY", 40.7505, -73.9934),
    ("90210", "Beverly Hills", "CA", 34.0901, -118.4065),
    ("60601", "Chicago", "IL", 41.8827, -87.6233),
    ("77001", "Houston", "TX", 29.7589, -95.3677),
    ("33101", "Miami", "FL", 25.7617, -80.1918),
    ("85001", "Phoenix", "AZ", 33.4734, -112.0740),
    ("19101", "Philadelphia", "PA", 39.9526, -75.1652),
    ("30301", "Atlanta", "GA", 33.7490, -84.3880),
    ("98101", "Seattle", "WA", 47.6062, -122.3321),
    ("80201", "Denver", "CO", 39.7392, -104.9903),
    ("48201", "Detroit", "MI", 42.3314, -83.0458),
    ("21201", "Baltimore", "MD", 39.2904, -76.6122),
    ("53201", "Milwaukee", "WI", 43.0389, -87.9065),
    ("87101", "Albuquerque", "NM", 35.0844, -106.6504),
    ("85701", "Tucson", "AZ", 32.2217, -110.9265),
    ("93701", "Fresno", "CA", 36.7378, -119.7871),
    ("95801", "Sacramento", "CA", 38.5816, -121.4944),
    ("64101", "Kansas City", "MO", 39.0997, -94.5786),
    ("85201", "Mesa", "AZ", 33.4152, -111.8315),
    ("23451", "Virginia Beach", "VA", 36.8529, -75.9780),
    ("80901", "Colorado Springs", "CO", 38.8339, -104.8214),
    ("68101", "Omaha", "NE", 41.2565, -95.9345),
    ("27601", "Raleigh", "NC", 35.7796, -78.6382),
    ("55401", "Minneapolis", "MN", 44.9778, -93.2650),
    ("74101", "Tulsa", "OK", 36.1540, -95.9928),
    ("44101", "Cleveland", "OH", 41.4993, -81.6944),
    ("67201", "Wichita", "KS", 37.6872, -97.3301),
    ("32801", "Orlando", "FL", 28.5383, -81.3792),
    ("70112", "New Orleans", "LA", 29.9511, -90.0715),
    ("37201", "Nashville", "TN", 36.1627, -86.7816),
    ("29201", "Columbia", "SC", 34.0007, -81.0348),
    ("72201", "Little Rock", "AR", 34.7465, -92.2896),
    ("59101", "Billings", "MT", 45.7833, -108.5007),
    ("83702", "Boise", "ID", 43.6150, -116.2023),
    ("97201", "Portland", "OR", 45.5152, -122.6784),
    ("84101", "Salt Lake City", "UT", 40.7608, -111.8910),
    ("89101", "Las Vegas", "NV", 36.1699, -115.1398),
    ("02101", "Boston", "MA", 42.3601, -71.0589),
    ("06101", "Hartford", "CT", 41.7658, -72.6734),
    ("08101", "Camden", "NJ", 39.9259, -75.1196),
    ("12201", "Albany", "NY", 42.6526, -73.7562),
    ("05401", "Burlington", "VT", 44.4759, -73.2121),
    ("03101", "Manchester", "NH", 42.9956, -71.4548),
    ("04101", "Portland", "ME", 43.6591, -70.2568),
    ("02801", "Warwick", "RI", 41.7001, -71.4162),
    ("50301", "Des Moines", "IA", 41.5868, -93.6250),
    ("58101", "Fargo", "ND", 46.8772, -96.7898),
    ("57101", "Sioux Falls", "SD", 43.5446, -96.7311),
    ("82001", "Cheyenne", "WY", 41.1400, -104.8197),
    ("99501", "Anchorage", "AK", 61.2181, -149.9003)
]

def generate_policy_number():
    """Generate a random policy number"""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    numbers = ''.join(random.choices('0123456789', k=8))
    return letters + numbers

def generate_policy_dates():
    """Generate realistic effective and expiration dates"""
    # Effective date could be in the past, present, or future
    base_date = datetime.now()
    effective_days_offset = random.randint(-730, 365)  # 2 years past to 1 year future
    effective_date = base_date + timedelta(days=effective_days_offset)
    
    # Expiration is typically 1 year after effective date
    expiration_date = effective_date + timedelta(days=365)
    
    return effective_date, expiration_date

def generate_policies():
    """Generate 50 policies using the standardized postal codes"""
    policy_types = ["Life Insurance", "Health Insurance", "Auto Insurance", "Property Insurance"]
    statuses = ["Policy Issued", "Policy Active", "Policy Expired", "Policy Cancelled"]
    
    policies = []
    
    for i in range(1, 51):  # Generate 50 policies
        # Choose a random postal code entry
        postal_code, city, state, latitude, longitude = random.choice(POSTAL_CODES)
        
        # Generate policy data
        policy_number = generate_policy_number()
        policy_type = random.choice(policy_types)
        effective_date, expiration_date = generate_policy_dates()
        status = random.choice(statuses)
        endorsement_amount = round(random.uniform(10000, 500000), 2)
        
        # Generate address
        street_number = random.randint(100, 9999)
        street_names = ["Main St", "Oak Ave", "First St", "Second Ave", "Park Blvd", 
                       "Elm St", "Cedar Ave", "Pine St", "Maple Dr", "Washington Ave"]
        address = f"{street_number} {random.choice(street_names)}"
        
        policy = [
            policy_number,          # PolicyNumber (string)
            policy_type,            # PolicyType (string)  
            effective_date.strftime('%Y-%m-%d'),  # EffectiveDate (string)
            expiration_date.strftime('%Y-%m-%d'), # ExpirationDate (string)
            status,                 # Status (string)
            endorsement_amount,     # EndorsementAmount (float)
            address,                # AddressLine (string)
            city,                   # City (string)
            state,                  # StateProvince (string)
            postal_code,            # PostalCode (string)
            "USA",                  # Country (string)
            latitude,               # Latitude (float)
            longitude               # Longitude (float)
        ]
        
        policies.append(policy)
    
    return policies

def write_csv(filename, data):
    """Write data to CSV file with proper quoting for non-integers"""
    header = [
        'PolicyNumber', 'PolicyType', 'EffectiveDate', 'ExpirationDate', 'Status',
        'EndorsementAmount', 'AddressLine', 'City', 'StateProvince', 'PostalCode', 
        'Country', 'Latitude', 'Longitude'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(header)
        
        for row in data:
            # Convert row to ensure proper types
            formatted_row = []
            for i, value in enumerate(row):
                if i in [5, 11, 12]:  # EndorsementAmount, Latitude, Longitude are numeric
                    formatted_row.append(value)
                else:  # All other fields are strings
                    formatted_row.append(str(value))
            writer.writerow(formatted_row)

if __name__ == "__main__":
    policies = generate_policies()
    write_csv('policy.csv', policies)
    print("Generated 50 rows of policy data in 'policy.csv'")
