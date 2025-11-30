"""ReportingAgent for generating formatted reports from LocationScoringResult data."""

import datetime
from typing import Optional
from .BaseAgent import BaseAgent
from .models.LocationScoringResult import LocationScoringResult


class ReportingAgent(BaseAgent):
    """Agent responsible for generating formatted reports from location scoring results."""
    
    def __init__(self):
        super().__init__(name="ReportingAgent")
        self.description = "Generates formatted reports from location scoring data using templates"
        self.template_path = "src/templates/SingleLocationReport.txt"
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return appropriate response."""
        return self.process_message(user_input)
    
    def process_message(self, message: str) -> str:
        """Process user messages related to report generation."""
        lower_message = message.lower()
        
        if "help" in lower_message:
            return self.get_help()
        elif "generate report" in lower_message or "create report" in lower_message:
            return "To generate a report, you need to provide a LocationScoringResult object. This is typically created by the Address Scoring Agent after evaluating a location's safety."
        elif "test report" in lower_message or "sample report" in lower_message or "demo report" in lower_message:
            return self.generate_sample_report()
        elif "template" in lower_message:
            return f"The reporting template is located at: {self.template_path}\nIt contains placeholders for location data, safety scores, and recommendations."
        else:
            return "I can generate reports from LocationScoringResult data. Use 'help' for more information, or try 'demo report' for a sample."
    
    def get_help(self) -> str:
        """Return help information for the ReportingAgent."""
        return """ReportingAgent Help:
        
Available commands:
- generate_location_report(scoring_result): Generate a formatted report from LocationScoringResult
- demo report: Generate a sample report with test data
- template: Show information about the report template
- help: Show this help message

I can create detailed reports showing:
- Location information (address, coordinates)
- Safety assessment scores and risk levels  
- Nearby superfund sites details
- Summary and recommendations
"""

    def generate_sample_report(self) -> str:
        """Generate a sample report with test data for demonstration purposes."""
        try:            
            # Import here to avoid circular imports
            from .models.Location import Location
            from .models.LocationScoringRequest import LocationScoringRequest
            from .models.LocationScoringResult import LocationScoringResult
            from .models.SuperFundSite import SuperFundSite
            import datetime

            # Create sample data
            test_location = Location(
                address="123 Demo Street",
                city="Sample City", 
                state_province="CA",
                postal_code="90210",
                country="USA",
                latitude=34.0522,
                longitude=-118.2437
            )
            
            scoring_request = LocationScoringRequest(
                location=test_location,
                radius_miles=50.0
            )


            # Create sample superfund site
            sample_site = SuperFundSite(
                site_name="Sample Superfund Site",
                location=test_location,
                pollution_class="Residential",
                pollution_type="Nuclear",
                remediation_status="Planned",
                remediation_start=datetime.datetime(2026, 5, 1),      
                remediation_finish=datetime.datetime(2027, 11, 30),   
                distance_miles=8.3
            )

            
            scoring_result = LocationScoringResult(
                request=scoring_request,
                nearby_superfund_sites=[sample_site]
            )

            return self.generate_location_report(scoring_result)
            
        except Exception as e:
            return f"Error generating sample report: {str(e)}"

    def generate_location_report(self, scoring_result: LocationScoringResult) -> str:
        """Generate a formatted report from LocationScoringResult using the template.
        
        Args:
            scoring_result: The LocationScoringResult object containing assessment data
            
        Returns:
            Formatted report string
        """
        try:
            # Load the template
            template_content = self._load_template()
            
            # Calculate safety metrics
            safety_score, risk_level, safety_percentage = self._calculate_safety_metrics(scoring_result)

            # Format the nearby sites details
            sites_details = self._format_nearby_sites(scoring_result.nearby_superfund_sites)

            # Generate summary and recommendations
            summary_text = self._generate_summary(scoring_result, safety_score, risk_level)

            recommendations = self._generate_recommendations(scoring_result, risk_level)

            # Create template variables
            template_vars = {
                'report_date': datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                'id': 1,
                'address': scoring_result.request.location.address,
                'city': scoring_result.request.location.city,
                'state_province': scoring_result.request.location.state_province,
                'postal_code': scoring_result.request.location.postal_code,
                'country': scoring_result.request.location.country,
                'latitude': scoring_result.request.location.latitude,
                'longitude': scoring_result.request.location.longitude,
                'safety_score': f"{safety_score:.1f}/10.0",
                'safety_percentage': safety_percentage,
                'risk_level': risk_level,
                'radius_miles': scoring_result.request.radius_miles,
                'sites_count': len(scoring_result.nearby_superfund_sites),
                'sites_details': sites_details,
                'summary_text': summary_text,
                'recommendations': recommendations
            }
            
            # Replace template placeholders
            formatted_report = template_content.format(**template_vars)
            return formatted_report
            
        except FileNotFoundError:
            return f"Error: Template file not found at {self.template_path}"
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _load_template(self) -> str:
        """Load the report template from file."""
        with open(self.template_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _calculate_safety_metrics(self, scoring_result: LocationScoringResult) -> tuple[float, str, str]:
        """Calculate safety score, risk level, and percentage based on nearby sites.
        
        Returns:
            Tuple of (safety_score, risk_level, safety_percentage)
        """
        sites_count = len(scoring_result.nearby_superfund_sites)
        
        # Simple scoring algorithm: subtract points for each nearby site
        base_score = 10.0
        score_reduction = min(sites_count * 1.5, 8.0)  # Max reduction of 8 points
        safety_score = max(base_score - score_reduction, 1.0)
        
        # Determine risk level
        if safety_score >= 8.0:
            risk_level = "LOW"
        elif safety_score >= 6.0:
            risk_level = "MODERATE"
        elif safety_score >= 4.0:
            risk_level = "HIGH"
        else:
            risk_level = "VERY HIGH"
        
        # Convert to percentage
        safety_percentage = f"{safety_score * 10:.0f}%"
        
        return safety_score, risk_level, safety_percentage
    
    def _format_nearby_sites(self, sites: list) -> str:
        """Format the list of nearby superfund sites for the report."""
        if not sites:
            return "No superfund sites found within the specified radius."
        
        formatted_sites = []
        for i, site in enumerate(sites, 1):
            site_info = f"""
Site #{i}:
  Name: site.site_name
  Address: {site.location.address}, {site.location.city}, {site.location.state_province} {site.location.postal_code}
  EPA ID: site.epa_id
  Status: site.npl_status
  Listed Date: site.date_npl_proposed.strftime('%m/%d/%Y') if site.date_npl_proposed else 'N/A'
  Final Date: site.date_npl_final.strftime('%m/%d/%Y') if site.date_npl_final else 'N/A'
"""
            formatted_sites.append(site_info)
        
        return "".join(formatted_sites)
    
    def _generate_summary(self, scoring_result: LocationScoringResult, safety_score: float, risk_level: str) -> str:
        """Generate a summary text for the report."""
        sites_count = len(scoring_result.nearby_superfund_sites)
        location = scoring_result.request.location
        radius = scoring_result.request.radius_miles
        
        if sites_count == 0:
            return f"The location at {location.address} shows excellent environmental safety with no known superfund sites within {radius} miles. This location presents minimal environmental risk."
        elif sites_count == 1:
            return f"The location at {location.address} has 1 superfund site within {radius} miles, resulting in a {risk_level.lower()} environmental risk rating. Consider the proximity and status of the nearby site when making location decisions."
        else:
            return f"The location at {location.address} has {sites_count} superfund sites within {radius} miles, resulting in a {risk_level.lower()} environmental risk rating. Multiple nearby sites indicate potential cumulative environmental concerns."
    
    def _generate_recommendations(self, scoring_result: LocationScoringResult, risk_level: str) -> str:
        """Generate recommendations based on the risk level."""
        sites_count = len(scoring_result.nearby_superfund_sites)
        
        if risk_level == "LOW":
            return "• Location appears environmentally safe for development or residence\n• Continue with standard environmental due diligence\n• Monitor EPA updates for any new superfund designations"
        elif risk_level == "MODERATE":
            return "• Conduct additional environmental assessment before major investments\n• Review specific contamination details of nearby sites\n• Consider soil and groundwater testing\n• Consult with environmental professionals"
        elif risk_level == "HIGH":
            return "• Strongly recommend comprehensive environmental assessment\n• Investigate contamination migration potential\n• Consider alternative locations for sensitive uses\n• Require detailed soil, air, and water quality testing"
        else:  # VERY HIGH
            return "• Exercise extreme caution - location not recommended for sensitive uses\n• Multiple superfund sites indicate significant environmental concerns\n• Extensive environmental remediation may be required\n• Strongly consider alternative locations\n• Consult with environmental remediation specialists"
