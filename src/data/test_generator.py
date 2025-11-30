import superfundsitesgenerator

sites = superfundsitesgenerator.generate_superfundsite_data()
superfundsitesgenerator.write_csv('superfundsites.csv', sites)
print(f"Generated {len(sites)} superfund sites")
