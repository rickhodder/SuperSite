from superfundsitesgenerator import generate_superfundsite_data, write_csv

sites = generate_superfundsite_data()
write_csv('new_superfundsites.csv', sites)
print(f"Generated {len(sites)} sites")
print(f"First site: {sites[0]}")
print("CSV created as new_superfundsites.csv")
