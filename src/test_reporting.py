"""Test script to demonstrate ReportingAgent functionality"""

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
    
    test_site1_location = Location(
        address="123 Main Street",
        city="Anytown", 
        state_province="CA",
        postal_code="90210",
        country="USA",
        latitude=34.0522,
        longitude=-118.2437
    )
    
    test_site2_location = Location(
        address="123 Main Street",
        city="Anytown", 
        state_province="CA",
        postal_code="90210",
        country="USA",
        latitude=34.0522,
        longitude=-118.2437
    )


    # Create some sample superfund sites
    site1 = SuperFundSite(
        #epa_id="CAD000123456",
        #site_name="Old Chemical Plant",
        location=test_site1_location,
        #address="456 Industrial Blvd",
        #city="Anytown",
        #state="CA",
        #zip_code="90211",
        #county="Los Angeles",
        #npl_status="Final",
        #date_npl_proposed=datetime(2010, 3, 15),
        #date_npl_final=datetime(2011, 8, 22),
        #latitude=34.0600,
        #longitude=-118.2500
        pollution_class="Industrial",
        pollution_type="Chemical Waste",
        remediation_status="Completed",
        remediation_start=datetime(2012, 5, 1),
        remediation_finish=datetime(2015, 11, 30),
        distance_miles=10.5
    )
    
    site2 = SuperFundSite(
        #epa_id="CAD000789012",
        #site_name="Former Gas Station",
        location=test_site2_location,        
        #address="789 Highway 101",
        #city="Nearby City",
        #state="CA",
        #zip_code="90212",
        #county="Los Angeles",
       #npl_status="Proposed",
        #date_npl_proposed=datetime(2020, 1, 10),
        #date_npl_final=None,
        #latitude=34.0400,
        #longitude=-118.2300
        pollution_class="Residential",
        pollution_type="uclear",
        remediation_status="Planned",
        remediation_start=datetime(2026, 5, 1),
        remediation_finish=datetime(2027, 11, 30),
        distance_miles=8.3
    )
    
    # Create scoring result
    scoring_result = LocationScoringResult(
        request=scoring_request,
        nearby_superfund_sites=[site1, site2]
    )
    print("got here")
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
