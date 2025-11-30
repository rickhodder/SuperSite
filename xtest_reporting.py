"""Test script to demonstrate ReportingAgent functionality"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.ReportingAgent import ReportingAgent
from agents.models.Location import Location
from agents.models.LocationScoringRequest import LocationScoringRequest
from agents.models.LocationScoringResult import LocationScoringResult
from agents.models.SuperFundSite import SuperFundSite
from datetime import datetime

def test_reporting_agent():
    """Test the ReportingAgent with sample data"""
    
    # Create a test location
    test_location = Location(
        address="123 Main Street",
        city="Anytown", 
        state_province="CA",
        postal_code="90210",
        country="USA",
        latitude=34.0522,
        longitude=-118.2437
    )
    
    # Create a scoring request
    scoring_request = LocationScoringRequest(
        location=test_location,
        radius_miles=50.0
    )
    
    # Create some sample superfund sites
    site1 = SuperFundSite(
        epa_id="CAD000123456",
        site_name="Old Chemical Plant",
        address="456 Industrial Blvd",
        city="Anytown",
        state="CA",
        zip_code="90211",
        county="Los Angeles",
        npl_status="Final",
        date_npl_proposed=datetime(2010, 3, 15),
        date_npl_final=datetime(2011, 8, 22),
        latitude=34.0600,
        longitude=-118.2500
    )
    
    site2 = SuperFundSite(
        epa_id="CAD000789012",
        site_name="Former Gas Station",
        address="789 Highway 101",
        city="Nearby City",
        state="CA",
        zip_code="90212",
        county="Los Angeles",
        npl_status="Proposed",
        date_npl_proposed=datetime(2020, 1, 10),
        date_npl_final=None,
        latitude=34.0400,
        longitude=-118.2300
    )
    
    # Create scoring result
    scoring_result = LocationScoringResult(
        request=scoring_request,
        nearby_superfund_sites=[site1, site2]
    )
    
    # Create and test the reporting agent
    reporting_agent = ReportingAgent()
    
    print("Testing ReportingAgent...")
    print("=" * 60)
    
    # Generate the report
    report = reporting_agent.generate_location_report(scoring_result)
    
    print(report)
    print("\n" + "=" * 60)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_reporting_agent()
