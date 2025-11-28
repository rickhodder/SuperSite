"""
SuperFund Sites Data Generator
Generates 50 superfund site records based on the SuperFundSite table definition
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

# Site name components
FIRST_NOUNS = [
    "Eagle", "Summit", "Valley", "River", "Mountain", "Forest", "Lake", "Stone", 
    "Cedar", "Pine", "Oak", "Maple", "Willow", "Granite", "Crystal", "Silver",
    "Golden", "Iron", "Copper", "Diamond", "Ruby", "Emerald", "Sunset", "Dawn",
    "Thunder", "Lightning", "Storm", "Wind", "Fire", "Water", "Earth", "Sky"
]

SECOND_NOUNS = [
    "Creek", "Ridge", "Hill", "Brook", "Grove", "Field", "Meadow", "Hollow",
    "Glen", "Dale", "Point", "Rock", "Peak", "Bluff", "Cove", "Bay", "Falls",
    "Springs", "Pond", "Mill", "Bridge", "Junction", "Crossing", "Plaza", "Park",
    "Gardens", "Heights", "Valley", "Vista", "Pointe", "Harbor", "Landing"
]

ALREADY_USED_SITE_NAMES = []

def generate_site_name():
    """Generate a site name with two random capitalized nouns followed by 'Site'"""    
    first_noun = random.choice(FIRST_NOUNS)
    second_noun = random.choice(SECOND_NOUNS)
    if f"{first_noun} {second_noun} Site" in ALREADY_USED_SITE_NAMES:
        return generate_site_name()
    ALREADY_USED_SITE_NAMES.append(f"{first_noun} {second_noun} Site")
    return f"{first_noun} {second_noun} Site"

def generate_fake_address():
    """Generate a fake address"""
    street_numbers = range(100, 9999)
    street_names = [
        "Industrial Blvd", "Factory Rd", "Chemical Ave", "Waste St", "Processing Ln", 
        "Manufacturing Dr", "Plant Ave", "Facility Rd", "Operations St", "Production Way",
        "Toxic Ave", "Hazmat Rd", "Environmental St", "Cleanup Ln", "Remediation Dr"
    ]
    return f"{random.choice(street_numbers)} {random.choice(street_names)}"

def generate_remediation_dates(status):
    """Generate remediation dates based on status"""
    if status == "Evaluating":
        return "", ""
    
    current_date = datetime.now()
    if status in ["In Progress", "Completed"]:
        start_date = current_date - timedelta(days=random.randint(1, 730))
    else:
        start_date = current_date + timedelta(days=random.randint(1, 180))
    
    if status == "Completed":
        finish_date = start_date + timedelta(days=random.randint(30, 365))
    elif status == "In Progress":
        finish_date = current_date + timedelta(days=random.randint(30, 365))
    else:
        finish_date = start_date + timedelta(days=random.randint(60, 365))
    
    return start_date.strftime('%Y-%m-%d'), finish_date.strftime('%Y-%m-%d')

# Generate data
data = []
for i in range(1, 51):
    postal_code, city, state, lat, lng = random.choice(POSTAL_CODES)
    site_name = generate_site_name()
    pollution_class = random.choice(["Industrial", "Federal", "Residential"])
    pollution_type = random.choice(["Nuclear", "Chemical", "Biological"])
    status = random.choice(["Evaluating", "Planned", "In Progress", "Completed"])
    
    start_date, finish_date = generate_remediation_dates(status)
    
    row = [i, site_name, pollution_class, pollution_type, status, start_date, finish_date, 
           generate_fake_address(), city, state, postal_code, "USA", lat, lng]
    data.append(row)
print("got here")
# Write CSV
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
            else:
                formatted_row.append(str(value))
        writer.writerow(formatted_row)

print("Generated 50 rows of superfundsite data in 'superfundsites.csv'")
