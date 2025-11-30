import csv
import os
from datetime import datetime
from .BaseAgent import BaseAgent
from .models.Policy import Policy
from .models.Location import Location

class PolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Policy Agent")
        self.csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'policy.csv')
        self.policies = []
        self.load_policies()
    
    def load_policies(self):
        """Load policies from CSV file and convert to Policy objects"""
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.policies = []                        
                for row in reader:
                    # Parse dates
                    effective_date = datetime.strptime(row['EffectiveDate'].strip('"'), '%Y-%m-%d')
                    expiration_date = datetime.strptime(row['ExpirationDate'].strip('"'), '%Y-%m-%d')
                    
                    # Create Location object
                    location = Location(
                        address=row['AddressLine'].strip('"'),
                        city=row['City'].strip('"'),
                        state_province=row['StateProvince'].strip('"'),
                        postal_code=row['PostalCode'].strip('"'),
                        country=row['Country'].strip('"'),
                        latitude=float(row['Latitude']), 
                        longitude=float(row['Longitude']),
                    )
                    
                    # Create Policy object
                    policy = Policy(
                        policy_number=row['PolicyNumber'].strip('"'),
                        policy_type=row['PolicyType'].strip('"'),
                        effective_date=effective_date,
                        expiration_date=expiration_date,
                        location=location,
                        status=row['Status'].strip('"'),
                        endorsement_amount=float(row['EndorsementAmount'])
                    )
                    self.policies.append(policy)
                    
            print(f"Loaded {len(self.policies)} Policy objects from CSV")
        except FileNotFoundError:
            print(f"Policy CSV file not found at: {self.csv_file}")
            self.policies = []
        except Exception as e:
            print(f"Error loading policies: {e}")
            self.policies = []
    
    def process_input(self, user_input):
        """Process user input and return policy information"""
        user_input_lower = user_input.lower()
        
        if "search policy" in user_input_lower:
            # Extract policy number or ID from input
            parts = user_input.split()
            if len(parts) > 2:
                search_term = parts[2].strip('"').upper()
                return self.search_policy(search_term)
            else:
                return "Please specify a policy number or ID. Example: 'search policy AB12345678' or 'search policy 5'"
        
        elif "list policies" in user_input_lower or "show all policies" in user_input_lower:
            return self.list_all_policies()
        
        elif "policy status" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 2:
                search_term = parts[2].strip('"').upper()
                return self.get_policy_status(search_term)
            else:
                return "Please specify a policy number or ID. Example: 'policy status AB12345678'"
        
        elif "count policies" in user_input_lower:
            return self.count_policies()
        
        elif "policies by status" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 3:
                status = ' '.join(parts[3:]).strip('"')
                return self.get_policies_by_status(status)
            else:
                return "Please specify a status. Example: 'policies by status Policy Issued'"
        
        elif "expired policies" in user_input_lower:
            return self.get_expired_policies()
        
        elif "help" in user_input_lower or "policy help" in user_input_lower:
            return self.show_help()
        
        else:
            return "I can help you with policy information. Type 'policy help' to see available commands."
    
    def process_task(self, task):
        """Process a specific policy-related task"""
        return self.process_input(task)
    
    def search_policy(self, search_term):
        """Search for a policy by ID or policy number"""
        for policy in self.policies:
            if policy.policy_number == search_term:
                return self.format_policy_details(policy)
        return f"Policy not found: {search_term}"
    
    def get_policy_status(self, search_term):
        """Get the status of a specific policy"""
        for policy in self.policies:
            if policy.policy_number == search_term:
                return f"Policy {policy.policy_number} status: {policy.status}"
        return f"Policy not found: {search_term}"
    
    def list_all_policies(self):
        """List all policies with specified fields"""
        if not self.policies:
            return "No policies loaded."
        
        result = f"All Policies ({len(self.policies)} found):\n\n"
        result += "ID | Policy Number | Policy Type   | Address                    | City          | State | Postal Code | Latitude  | Longitude\n"
        result += "-" * 140 + "\n"
        
        for i, policy in enumerate(self.policies, 1):
            result += f"{i:2} | {policy.policy_number:13} | {policy.policy_type:13} | {policy.location.address:26} | {policy.location.city:13} | {policy.location.state_province:5} | {policy.location.postal_code:11} | {policy.location.latitude:9.4f} | {policy.location.longitude:9.4f}\n"
        
        return result
    
    def count_policies(self):
        """Count policies by status"""
        if not self.policies:
            return "No policies loaded."
        
        status_counts = {}
        for policy in self.policies:
            status_counts[policy.status] = status_counts.get(policy.status, 0) + 1
        
        result = f"Total Policies: {len(self.policies)}\n\nPolicy Count by Status:\n"
        for status, count in status_counts.items():
            result += f"  {status}: {count}\n"
        
        return result
    
    def get_policies_by_status(self, status):
        """Get all policies with a specific status"""
        matching_policies = [p for p in self.policies if p.status.lower() == status.lower()]
        
        if not matching_policies:
            return f"No policies found with status: {status}"
        
        result = f"Policies with status '{status}' ({len(matching_policies)} found):\n\n"
        result += "Policy Number | Location                    | Expiration\n"
        result += "-" * 60 + "\n"
        
        for policy in matching_policies:
            location_str = f"{policy.location.city}, {policy.location.state_province}"
            result += f"{policy.policy_number:12} | {location_str:27} | {policy.expiration_date.strftime('%Y-%m-%d')}\n"
        
        return result
    
    def get_expired_policies(self):
        """Get policies that have expired"""
        current_date = datetime.now().date()
        expired_policies = [p for p in self.policies if p.expiration_date.date() < current_date]
        
        if not expired_policies:
            return "No expired policies found."
        
        result = f"Expired Policies ({len(expired_policies)} found):\n\n"
        result += "Policy Number | Status        | Location              | Expired\n"
        result += "-" * 70 + "\n"
        
        for policy in expired_policies:
            location_str = f"{policy.location.city}, {policy.location.state_province}"
            result += f"{policy.policy_number:12} | {policy.status:13} | {location_str:20} | {policy.expiration_date.strftime('%Y-%m-%d')}\n"
        
        return result
    
    def format_policy_details(self, policy):
        """Format complete policy details"""
        result = f"Policy Details:\n"
        result += f"  Policy Number: {policy.policy_number}\n"
        result += f"  Status: {policy.status}\n"
        result += f"  Effective Date: {policy.effective_date.strftime('%Y-%m-%d')}\n"
        result += f"  Expiration Date: {policy.expiration_date.strftime('%Y-%m-%d')}\n"
        result += f"  Address: {policy.location.address}\n"
        result += f"  City: {policy.location.city}, {policy.location.state_province} {policy.location.postal_code}\n"
        result += f"  Country: {policy.location.country}\n"
        if policy.endorsement_amount != 0:
            result += f"  Endorsement Amount: ${policy.endorsement_amount:,.2f}\n"
        
        return result
    
    def show_help(self):
        """Show available policy commands"""
        help_text = """
Policy Agent Commands:
- 'search policy [ID/PolicyNumber]' - Get full details of a policy
- 'policy status [ID/PolicyNumber]' - Get status of a specific policy
- 'list policies' or 'show all policies' - List all policies
- 'count policies' - Show count of policies by status
- 'policies by status [status]' - Show policies with specific status
- 'expired policies' - Show all expired policies
- 'policy help' - Show this help message

Examples:
- search policy 5
- search policy AB12345678
- policy status SE92875388
- policies by status Policy Issued
- count policies
        """
        return help_text.strip()
