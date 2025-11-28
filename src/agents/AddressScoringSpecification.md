Need an AddressScoringAgent that when given an address or at least a postal code
will search through the data\superfundsites.csv looking for sites that are within 50 miles of the input address (could be multiple sites)
and return a safety score between 0 and 1 based on the following rules:
The agent should return an object that contains the score, and a list of of the superfund sites that fall within 50 miles
if no sites are found within 50 miles of an address, it should return a score of 1 (100%) signifying that the address is safe
if one or more sites are found within 50 miles of a site, for each site, it should lower the score by .25  signifying that the address is less safe
but never lower the score below 0 (0%)
