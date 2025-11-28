"""PolicyProcessingAgent for processing policies and evaluating their locations using address scoring."""

import os
from typing import Optional, Dict
from .BaseAgent import BaseAgent
from .PolicyAgent import PolicyAgent
from .AddressScoringAgent import AddressScoringAgent
from .models.LocationScoringResult import LocationScoringResult
from .models.Policy import Policy

class PolicyProcessingAgent(BaseAgent):
    """Agent that processes policies and evaluates their locations using address scoring."""
    
    def __init__(self):
        super().__init__("Policy Processing Agent")
        self.description = "Processes policies and evaluates location safety using address scoring"
        
        # Initialize sub-agents
        self.policy_agent = PolicyAgent()
        self.address_scoring_agent = AddressScoringAgent()
    
    def process_input(self, user_input: str) -> str:
        """Process user input and route to appropriate methods"""
        user_input_lower = user_input.lower()
        
        if "help" in user_input_lower or "policy help" in user_input_lower:
            return self.show_help()
        
        elif user_input_lower.startswith("process policy"):
            # Extract policy number from command
            parts = user_input.split(" ", 2)
            if len(parts) >= 3:
                policy_number = parts[2].strip()
                return self.process_policy_location_safety(policy_number)
            else:
                return "Please provide a policy number. Example: 'process policy AB12345678'"
        
        elif user_input_lower.startswith("evaluate policy"):
            # Extract policy number from command
            parts = user_input.split(" ", 2)
            if len(parts) >= 3:
                policy_number = parts[2].strip()
                return self.process_policy_location_safety(policy_number)
            else:
                return "Please provide a policy number. Example: 'evaluate policy AB12345678'"
        
        elif user_input_lower.startswith("safety check policy"):
            # Extract policy number from command
            parts = user_input.split(" ", 3)
            if len(parts) >= 4:
                policy_number = parts[3].strip()
                return self.process_policy_location_safety(policy_number)
            else:
                return "Please provide a policy number. Example: 'safety check policy AB12345678'"
        
        elif "list policies" in user_input_lower:
            return self.list_available_policies()
        
        elif user_input_lower.startswith("policy details"):
            # Extract policy number from command
            parts = user_input.split(" ", 2)
            if len(parts) >= 3:
                policy_number = parts[2].strip()
                return self.get_policy_details_only(policy_number)
            else:
                return "Please provide a policy number. Example: 'policy details AB12345678'"
        
        # Check if input looks like a policy number (2 letters + 8 digits)
        elif self.is_policy_number(user_input.strip()):
            return self.process_policy_location_safety(user_input.strip())
        
        else:
            return "I can process policies and evaluate their location safety. Type 'help' to see available commands."
    
    def examine_evaluation(self,policy_number: str) -> str:
        try:
            # Step 1: Get policy information
            policy = self.find_policy(policy_number)
            if not policy:
                return f"❌ Policy not found: {policy_number}\n\nAvailable policies can be viewed with 'list policies' command."
            
            # Step 2: Format policy address for address scoring
            policy_address = self.format_policy_address(policy)
            
            # Step 3: Evaluate location safety
            scoring_result = self.address_scoring_agent.evaluate_address_safety(policy_address)
            
            # Step 4: Determine action based on scoring result
            action = self.determine_action(policy, scoring_result)

            print(action)
            return action
        
        except Exception as e:
            return f"❌ Error processing policy {policy_number}: {str(e)}"
        
    # turn this into something that changes the policy status
    def determine_action(self,policy:Policy, scoring_result:LocationScoringResult) -> str:
        if(scoring_result.count_nearby_sites == 0):
            return "✅ APPROVE POLICY - Location is safe."

        if(scoring_result.count_nearby_sites >0):
            if(scoring_result.nearby_superfund_sites[0].pollution_type=='Nuclear'):
                policy.status = "Cancelled"
                return "❌ CANCEL POLICY - Location near nuclear contamination site."
            elif(scoring_result.nearby_superfund_sites[0].pollution_type=='Chemical' and scoring_result.nearby_superfund_sites[0].remediation_finish is not None):
                policy.status = "Policy Issued"
                return "✅ APPROVE POLICY - Location has been remediatated."
            elif(scoring_result.nearby_superfund_sites[0].pollution_type=='Hazardous' and scoring_result.nearby_superfund_sites[0].remediation_finish is not None):
                policy.status = "Endorsement Added"
                policy.endorsement_amount = 5000  # Example endorsement amount
                return "⚠️ Add Endorsement - increase in premium recommended due to nearby remediated hazardous site."
            else:
                policy.status = "Policy Issued"
                return "✅ APPROVE POLICY - Location is safe."

    def process_task(self, task):
        """Process a specific policy processing task"""
        return self.process_input(task)
    
    def process_policy_location_safety(self, policy_number: str) -> str:
        """
        Process a policy by policy number and evaluate its location safety
        
        Args:
            policy_number: The policy number to process
            
        Returns:
            Formatted report with policy details and location safety assessment
        """
        try:
            # Step 1: Get policy information
            policy = self.find_policy(policy_number)
            if not policy:
                return f"❌ Policy not found: {policy_number}\n\nAvailable policies can be viewed with 'list policies' command."
            
            # Step 2: Format policy address for address scoring
            policy_address = self.format_policy_address(policy)
            
            # Step 3: Evaluate location safety
            safety_result = self.address_scoring_agent.evaluate_address_safety(policy_address)
            
            # Step 4: Generate comprehensive report
            return self.generate_policy_safety_report(policy, safety_result, policy_address)
            
        except Exception as e:
            return f"❌ Error processing policy {policy_number}: {str(e)}"
    
    def find_policy(self, policy_number: str):
        """Find a policy by policy number"""
        for policy in self.policy_agent.policies:
            if policy.policy_number == policy_number:
                return policy
        return None
    
    def format_policy_address(self, policy) -> str:
        """Format policy location as an address string for scoring"""
        address_parts = [
            policy.location.address,
            f"{policy.location.city}, {policy.location.state_province}",
            policy.location.postal_code
        ]
        return ", ".join(filter(None, address_parts))
    
    def generate_policy_safety_report(self, policy, safety_result: Dict, formatted_address: str) -> str:
        """Generate a comprehensive policy and safety report"""
        # Policy section
        report = "🏢 POLICY LOCATION SAFETY ASSESSMENT\n"
        report += "=" * 50 + "\n\n"
        
        # Policy Details
        report += "📋 POLICY INFORMATION:\n"
        report += f"   Policy Number: {policy.policy_number}\n"
        report += f"   Status: {policy.status}\n"
        report += f"   Effective Date: {policy.effective_date.strftime('%Y-%m-%d')}\n"
        report += f"   Expiration Date: {policy.expiration_date.strftime('%Y-%m-%d')}\n"
        if policy.endorsement_amount > 0:
            report += f"   Endorsement Amount: ${policy.endorsement_amount:,.2f}\n"
        
        # Location Details
        report += f"\n📍 POLICY LOCATION:\n"
        report += f"   Address: {policy.location.address}\n"
        report += f"   City: {policy.location.city}, {policy.location.state_province} {policy.location.postal_code}\n"
        report += f"   Country: {policy.location.country}\n"
        report += f"   Formatted Address: {formatted_address}\n"
        
        # Safety Assessment
        report += f"\n🛡️ LOCATION SAFETY ASSESSMENT:\n"
        
        if "error" in safety_result:
            report += f"   ❌ Error: {safety_result['error']}\n"
        else:
            score = safety_result['score']
            nearby_sites = safety_result['nearby_sites']
            sites_count = len(nearby_sites)
            percentage = f"{score * 100:.1f}%"
            
            # Determine safety level
            if score == 1.0:
                safety_level = "COMPLETELY SAFE"
                emoji = "🟢"
            elif score >= 0.75:
                safety_level = "MOSTLY SAFE"
                emoji = "🟡"
            elif score >= 0.5:
                safety_level = "MODERATE RISK"
                emoji = "🟠"
            elif score > 0:
                safety_level = "HIGH RISK"
                emoji = "🔴"
            else:
                safety_level = "MAXIMUM RISK"
                emoji = "🚨"
            
            report += f"   {emoji} Safety Score: {percentage} - {safety_level}\n"
            report += f"   📊 Superfund Sites within 50 miles: {sites_count}\n"
            
            # Risk Assessment for Insurance
            if score >= 0.75:
                risk_assessment = "LOW RISK - Standard coverage recommended"
            elif score >= 0.5:
                risk_assessment = "MODERATE RISK - Enhanced environmental coverage suggested"
            elif score > 0.25:
                risk_assessment = "HIGH RISK - Comprehensive environmental coverage required"
            else:
                risk_assessment = "VERY HIGH RISK - Specialized environmental coverage mandatory"
            
            report += f"   📈 Insurance Risk Assessment: {risk_assessment}\n"
            
            # Nearby Sites Details
            if sites_count > 0:
                report += f"\n🏭 NEARBY SUPERFUND SITES:\n"
                for i, site in enumerate(nearby_sites, 1):
                    report += f"   {i}. {site.pollution_class} Site ({site.distance_miles} miles)\n"
                    report += f"      📍 {site.location.address}, {site.location.city}, {site.location.state_province}\n"
                    report += f"      🏭 Type: {site.pollution_class} - {site.pollution_type}\n"
                    report += f"      🔧 Status: {site.remediation_status}\n"
                    
                    if site.remediation_start:
                        report += f"      📅 Start: {site.remediation_start.strftime('%Y-%m-%d')}\n"
                    if site.remediation_finish:
                        report += f"      📅 Finish: {site.remediation_finish.strftime('%Y-%m-%d')}\n"
                    report += "\n"
            else:
                report += f"\n✅ No superfund sites found within 50 miles of policy location!\n"
        
        # Recommendations
        report += f"\n💡 RECOMMENDATIONS:\n"
        if "error" not in safety_result:
            if safety_result['score'] >= 0.75:
                report += "   • Standard policy terms are appropriate\n"
                report += "   • Regular monitoring sufficient\n"
            elif safety_result['score'] >= 0.5:
                report += "   • Consider environmental liability coverage\n"
                report += "   • Monitor nearby remediation progress\n"
            elif safety_result['score'] > 0.25:
                report += "   • Require environmental assessment\n"
                report += "   • Implement enhanced monitoring\n"
                report += "   • Consider premium adjustments\n"
            else:
                report += "   • Mandatory environmental impact assessment\n"
                report += "   • Specialized underwriting required\n"
                report += "   • Consider policy restrictions\n"
        else:
            report += "   • Complete location verification required\n"
            report += "   • Manual underwriting recommended\n"
        
        return report
    
    def get_policy_details_only(self, policy_number: str) -> str:
        """Get only policy details without safety assessment"""
        policy = self.find_policy(policy_number)
        if not policy:
            return f"❌ Policy not found: {policy_number}"
        
        # Format policy details
        details = f"📋 POLICY DETAILS:\n"
        details += f"Policy Number: {policy.policy_number}\n"
        details += f"Status: {policy.status}\n"
        details += f"Effective Date: {policy.effective_date.strftime('%Y-%m-%d')}\n"
        details += f"Expiration Date: {policy.expiration_date.strftime('%Y-%m-%d')}\n"
        if policy.endorsement_amount > 0:
            details += f"Endorsement Amount: ${policy.endorsement_amount:,.2f}\n"
        details += f"\nLocation:\n"
        details += f"  Address: {policy.location.address}\n"
        details += f"  City: {policy.location.city}, {policy.location.state_province} {policy.location.postal_code}\n"
        details += f"  Country: {policy.location.country}\n"
        
        return details
    
    def list_available_policies(self) -> str:
        """List all available policies"""
        return self.policy_agent.list_all_policies()
    
    def is_policy_number(self, input_str: str) -> bool:
        """Check if input looks like a policy number (2 letters + 8 digits)"""
        import re
        pattern = r'^[A-Za-z]{2}\d{8}$'
        return bool(re.match(pattern, input_str))
    
    def show_help(self) -> str:
        """Show available policy processing commands"""
        help_text = """
🏢 POLICY PROCESSING AGENT COMMANDS:

📋 Policy Processing:
• process policy [policy_number] - Evaluate policy location safety
• evaluate policy [policy_number] - Same as process policy
• safety check policy [policy_number] - Comprehensive safety assessment
• [policy_number] - Direct policy number input (e.g., AB12345678)

📊 Policy Information:
• policy details [policy_number] - Get policy details only
• list policies - Show all available policies

📍 Examples:
• process policy AB12345678
• evaluate policy CD98765432
• safety check policy EF11223344
• AB12345678 (direct input)

🔍 What this agent does:
1. Retrieves policy information by policy number
2. Extracts the policy location address
3. Calls AddressScoringAgent to evaluate location safety
4. Generates comprehensive report with:
   - Policy details and status
   - Location information
   - Safety score based on nearby superfund sites
   - Risk assessment for insurance purposes
   - Recommendations for underwriting

📝 Note: Policy numbers should be in format: 2 letters + 8 digits (e.g., AB12345678)
        """
        return help_text.strip()
