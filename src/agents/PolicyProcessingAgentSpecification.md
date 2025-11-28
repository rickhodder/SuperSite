# PolicyProcessingAgent Specification

## Overview
The PolicyProcessingAgent is a composite agent that combines policy lookup functionality with location safety assessment. It accepts a policy number, retrieves the policy information, and evaluates the safety of the policy's location using the AddressScoringAgent.

## Purpose
- Bridge policy management with environmental risk assessment
- Provide comprehensive policy location safety evaluation
- Generate insurance underwriting recommendations
- Support environmental risk-based decision making

## Class: PolicyProcessingAgent

### Dependencies
- **BaseAgent**: Inherits core agent functionality
- **PolicyAgent**: Sub-agent for policy data retrieval
- **AddressScoringAgent**: Sub-agent for location safety evaluation

### Key Methods

#### `process_policy_location_safety(policy_number: str) -> str`
**Primary Method**: Processes a policy and evaluates location safety.

**Workflow:**
1. Look up policy by policy number using PolicyAgent
2. Extract and format policy location address
3. Call AddressScoringAgent to evaluate location safety
4. Generate comprehensive report combining policy and safety data

**Returns**: Formatted comprehensive report

#### `find_policy(policy_number: str)`
Searches for a policy by policy number in the PolicyAgent's data.

#### `format_policy_address(policy) -> str`
Converts policy Location object to address string suitable for AddressScoringAgent input.

#### `generate_policy_safety_report(policy, safety_result: Dict, formatted_address: str) -> str`
Creates comprehensive report including:
- 📋 Policy details (number, status, dates, endorsement)
- 📍 Location information
- 🛡️ Safety assessment with scoring
- 📈 Insurance risk assessment
- 🏭 Nearby superfund sites details
- 💡 Underwriting recommendations

### Commands Supported

#### Policy Processing Commands
- `process policy [policy_number]` - Full evaluation
- `evaluate policy [policy_number]` - Same as process
- `safety check policy [policy_number]` - Comprehensive safety assessment
- `[policy_number]` - Direct input (auto-detected format: 2 letters + 8 digits)

#### Information Commands
- `policy details [policy_number]` - Policy info only (no safety assessment)
- `list policies` - Show all available policies
- `help` - Show command reference

### Policy Number Format
- Pattern: `^[A-Za-z]{2}\d{8}$`
- Examples: AB12345678, CD98765432, EF11223344

### Integration Points

#### With PolicyAgent
- Uses `policies` list to find policy by number
- Accesses Policy objects with Location data
- Formats policy details for display

#### With AddressScoringAgent
- Calls `evaluate_address_safety(address)` method
- Receives safety score and nearby sites data
- Interprets results for insurance context

### Report Structure

#### Section 1: Policy Information
```
🏢 POLICY LOCATION SAFETY ASSESSMENT
==================================================

📋 POLICY INFORMATION:
   Policy Number: AB12345678
   Status: Policy Issued
   Effective Date: 2024-01-15
   Expiration Date: 2025-01-15
   Endorsement Amount: $25,000.00
```

#### Section 2: Location Details
```
📍 POLICY LOCATION:
   Address: 123 Main Street
   City: Anytown, CA 90210
   Country: USA
   Formatted Address: 123 Main Street, Anytown, CA, 90210
```

#### Section 3: Safety Assessment
```
🛡️ LOCATION SAFETY ASSESSMENT:
   🟢 Safety Score: 75.0% - MOSTLY SAFE
   📊 Superfund Sites within 50 miles: 1
   📈 Insurance Risk Assessment: LOW RISK - Standard coverage recommended
```

#### Section 4: Nearby Sites (if any)
```
🏭 NEARBY SUPERFUND SITES:
   1. Industrial Site (25.3 miles)
      📍 456 Industrial Way, Industrial City, CA
      🏭 Type: Industrial - Chemical
      🔧 Status: In Progress
      📅 Start: 2023-03-01
      📅 Finish: 2025-12-31
```

#### Section 5: Recommendations
```
💡 RECOMMENDATIONS:
   • Standard policy terms are appropriate
   • Regular monitoring sufficient
```

### Insurance Risk Assessment Levels

- **LOW RISK** (75-100%): Standard coverage recommended
- **MODERATE RISK** (50-74%): Enhanced environmental coverage suggested  
- **HIGH RISK** (25-49%): Comprehensive environmental coverage required
- **VERY HIGH RISK** (0-24%): Specialized environmental coverage mandatory

### Use Cases

1. **Policy Underwriting**: Assess environmental risk for new policies
2. **Policy Renewal Review**: Evaluate existing policies for location-based risks
3. **Risk Assessment**: Determine appropriate coverage levels and premiums
4. **Regulatory Compliance**: Check policies against environmental exposure requirements
5. **Claims Prevention**: Identify high-risk locations for proactive measures

### Error Handling
- Policy not found scenarios
- Address formatting issues  
- AddressScoringAgent evaluation errors
- Missing or invalid policy data
- Postal code resolution failures

### Console Integration
- Added as Agent #6 in the console interface
- Supports all standard agent operations (help, process_input, process_task)
- Integrates with existing chat handler system
