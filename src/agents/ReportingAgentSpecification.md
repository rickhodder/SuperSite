# ReportingAgent Specification

## Overview
The ReportingAgent is responsible for generating formatted reports from LocationScoringResult data using predefined templates. It transforms raw scoring data into professional, human-readable reports suitable for decision-making.

## Purpose
- Convert LocationScoringResult objects into formatted reports
- Provide standardized report formatting using templates
- Calculate and present safety metrics in an understandable format
- Generate actionable recommendations based on risk assessment

## Key Methods

### process_message(message: str) -> str
Handles user interaction and command routing for report generation requests.

### generate_location_report(scoring_result: LocationScoringResult) -> str
**Primary Method**: Generates a comprehensive location safety report.

**Input**: LocationScoringResult object containing:
- LocationScoringRequest (location and search radius)
- List of nearby SuperFundSite objects

**Output**: Formatted string report containing:
- Location information (address, coordinates)
- Safety assessment scores and risk levels
- Detailed nearby superfund sites information
- Summary analysis
- Risk-based recommendations

## Safety Scoring Algorithm
- Base Score: 10.0 points (perfect safety)
- Score Reduction: 1.5 points per nearby superfund site
- Maximum Reduction: 8.0 points (minimum score of 1.0)
- Risk Levels:
  - 8.0-10.0: LOW risk
  - 6.0-7.9: MODERATE risk  
  - 4.0-5.9: HIGH risk
  - 1.0-3.9: VERY HIGH risk

## Template System
Uses `SingleLocationReport.template` with the following placeholders:
- {report_date} - Current date and time
- {assessment_id} - Unique report identifier
- {address}, {city}, {state_province}, {postal_code}, {country} - Location details
- {latitude}, {longitude} - Coordinates
- {safety_score} - Calculated safety score out of 10
- {safety_percentage} - Score as percentage
- {risk_level} - Risk category (LOW/MODERATE/HIGH/VERY HIGH)
- {radius_miles} - Search radius used
- {sites_count} - Number of nearby superfund sites
- {sites_details} - Formatted list of site information
- {summary_text} - Generated summary
- {recommendations} - Risk-appropriate recommendations

## Integration
- Inherits from BaseAgent
- Can be integrated into console interface as fifth agent option
- Designed to work with output from AddressScoringAgent
- Uses models from the models folder (LocationScoringResult, LocationScoringRequest, SuperFundSite, Location)

## Error Handling
- Template file not found errors
- Invalid LocationScoringResult data
- Template formatting errors
- Graceful degradation with error messages
