import csv
import os
from agents.BaseAgent import BaseAgent

class SuperFundSiteAgent(BaseAgent):
    def __init__(self):
        super().__init__("SuperFund Site Agent")
        self.csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'superfundsites.csv')
        self.sites = []
        self.load_sites()
    
    def load_sites(self):
        """Load superfund sites from CSV file"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.sites = list(reader)
            print(f"Loaded {len(self.sites)} superfund sites from CSV")
        except FileNotFoundError:
            print(f"SuperFund sites CSV file not found at: {self.csv_file}")
            self.sites = []
        except Exception as e:
            print(f"Error loading superfund sites: {e}")
            self.sites = []
    
    def process_input(self, user_input):
        """Process user input and return superfundsite information"""
        user_input_lower = user_input.lower()
        
        if "search site" in user_input_lower:
            # Extract site ID from input
            parts = user_input.split()
            if len(parts) > 2:
                search_term = parts[2].strip()
                return self.search_site(search_term)
            else:
                return "Please specify a site ID. Example: 'search site 5'"
        
        elif "list sites" in user_input_lower or "show all sites" in user_input_lower:
            return self.list_all_sites()
        
        elif "site status" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 2:
                search_term = parts[2].strip()
                return self.get_site_status(search_term)
            else:
                return "Please specify a site ID. Example: 'site status 5'"
        
        elif "count sites" in user_input_lower:
            return self.count_sites()
        
        elif "sites by pollution" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 3:
                pollution_type = ' '.join(parts[3:]).strip('"')
                return self.get_sites_by_pollution(pollution_type)
            else:
                return "Please specify a pollution type. Example: 'sites by pollution Nuclear'"
        
        elif "sites by class" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 3:
                pollution_class = ' '.join(parts[3:]).strip('"')
                return self.get_sites_by_class(pollution_class)
            else:
                return "Please specify a pollution class. Example: 'sites by class Industrial'"
        
        elif "sites by status" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 3:
                status = ' '.join(parts[3:]).strip('"')
                return self.get_sites_by_status(status)
            else:
                return "Please specify a remediation status. Example: 'sites by status In Progress'"
        
        elif "evaluating sites" in user_input_lower:
            return self.get_evaluating_sites()
        
        elif "completed sites" in user_input_lower:
            return self.get_completed_sites()
        
        elif "sites by city" in user_input_lower:
            parts = user_input.split()
            if len(parts) > 3:
                city = ' '.join(parts[3:]).strip('"')
                return self.get_sites_by_city(city)
            else:
                return "Please specify a city. Example: 'sites by city Houston'"
        
        elif "help" in user_input_lower or "site help" in user_input_lower:
            return self.show_help()
        
        else:
            return "I can help you with superfund site information. Type 'site help' to see available commands."
    
    def process_task(self, task):
        """Process a specific superfund site-related task"""
        return self.process_input(task)
    
    def search_site(self, search_term):
        """Search for a site by ID"""
        for site in self.sites:
            if site['Id'] == search_term:
                return self.format_site_details(site)
        return f"Site not found: {search_term}"
    
    def get_site_status(self, search_term):
        """Get the remediation status of a specific site"""
        for site in self.sites:
            if site['Id'] == search_term:
                status = site['RemediationStatus'].strip('"')
                pollution_class = site['PollutionClass'].strip('"')
                pollution_type = site['PollutionType'].strip('"')
                return f"Site {search_term} - {pollution_class} {pollution_type} contamination - Status: {status}"
        return f"Site not found: {search_term}"
    
    def list_all_sites(self):
        """List all sites with complete information"""
        if not self.sites:
            return "No sites loaded."
        
        result = f"Total SuperFund Sites: {len(self.sites)}\n\n"
        result += "ID | Class       | Type        | Status        | Postal        | Start Date   | End Date     | Latitude  | Longitude\n"
        result += "-" * 130 + "\n"
        
        for site in self.sites:
            site_id = site['Id']
            pollution_class = site['PollutionClass'].strip('"')
            pollution_type = site['PollutionType'].strip('"')
            status = site['RemediationStatus'].strip('"')
            postal_code = site['PostalCode'].strip('"')
            start_date = site['RemediationStart'].strip('"') or "N/A"
            end_date = site['RemediationFinish'].strip('"') or "N/A"
            latitude = float(site['Latitude'])
            longitude = float(site['Longitude'])
            result += f"{site_id:2} | {pollution_class:11} | {pollution_type:11} | {status:13} | {postal_code:13} | {start_date:12} | {end_date:12} | {latitude:9.4f} | {longitude:9.4f}\n"
        
        return result
    
    def count_sites(self):
        """Count sites by various categories"""
        if not self.sites:
            return "No sites loaded."
        
        # Count by pollution class
        class_counts = {}
        type_counts = {}
        status_counts = {}
        
        for site in self.sites:
            pollution_class = site['PollutionClass'].strip('"')
            pollution_type = site['PollutionType'].strip('"')
            status = site['RemediationStatus'].strip('"')
            
            class_counts[pollution_class] = class_counts.get(pollution_class, 0) + 1
            type_counts[pollution_type] = type_counts.get(pollution_type, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1
        
        result = f"Total Sites: {len(self.sites)}\n\n"
        
        result += "Sites by Pollution Class:\n"
        for class_type, count in class_counts.items():
            result += f"  {class_type}: {count}\n"
        
        result += "\nSites by Pollution Type:\n"
        for pollution_type, count in type_counts.items():
            result += f"  {pollution_type}: {count}\n"
        
        result += "\nSites by Remediation Status:\n"
        for status, count in status_counts.items():
            result += f"  {status}: {count}\n"
        
        return result
    
    def get_sites_by_pollution(self, pollution_type):
        """Get all sites with a specific pollution type"""
        matching_sites = [s for s in self.sites if s['PollutionType'].strip('"').lower() == pollution_type.lower()]
        
        if not matching_sites:
            return f"No sites found with pollution type: {pollution_type}"
        
        result = f"Sites with {pollution_type} pollution ({len(matching_sites)} found):\n\n"
        result += "ID | Class       | Status        | City           | Address\n"
        result += "-" * 70 + "\n"
        
        for site in matching_sites:
            site_id = site['Id']
            pollution_class = site['PollutionClass'].strip('"')
            status = site['RemediationStatus'].strip('"')
            city = site['City'].strip('"')
            address = site['AddressLine'].strip('"')
            result += f"{site_id:2} | {pollution_class:11} | {status:13} | {city:14} | {address}\n"
        
        return result
    
    def get_sites_by_class(self, pollution_class):
        """Get all sites with a specific pollution class"""
        matching_sites = [s for s in self.sites if s['PollutionClass'].strip('"').lower() == pollution_class.lower()]
        
        if not matching_sites:
            return f"No sites found with pollution class: {pollution_class}"
        
        result = f"{pollution_class} sites ({len(matching_sites)} found):\n\n"
        result += "ID | Type        | Status        | City           | State\n"
        result += "-" * 60 + "\n"
        
        for site in matching_sites:
            site_id = site['Id']
            pollution_type = site['PollutionType'].strip('"')
            status = site['RemediationStatus'].strip('"')
            city = site['City'].strip('"')
            state = site['StateProvince'].strip('"')
            result += f"{site_id:2} | {pollution_type:11} | {status:13} | {city:14} | {state}\n"
        
        return result
    
    def get_sites_by_status(self, status):
        """Get all sites with a specific remediation status"""
        matching_sites = [s for s in self.sites if s['RemediationStatus'].strip('"').lower() == status.lower()]
        
        if not matching_sites:
            return f"No sites found with status: {status}"
        
        result = f"Sites with status '{status}' ({len(matching_sites)} found):\n\n"
        result += "ID | Class       | Type        | City           | Start Date   | End Date\n"
        result += "-" * 75 + "\n"
        
        for site in matching_sites:
            site_id = site['Id']
            pollution_class = site['PollutionClass'].strip('"')
            pollution_type = site['PollutionType'].strip('"')
            city = site['City'].strip('"')
            start_date = site['RemediationStart'].strip('"') or "N/A"
            end_date = site['RemediationFinish'].strip('"') or "N/A"
            result += f"{site_id:2} | {pollution_class:11} | {pollution_type:11} | {city:14} | {start_date:12} | {end_date}\n"
        
        return result
    
    def get_evaluating_sites(self):
        """Get all sites currently being evaluated"""
        return self.get_sites_by_status("Evaluating")
    
    def get_completed_sites(self):
        """Get all completed remediation sites"""
        return self.get_sites_by_status("Completed")
    
    def get_sites_by_city(self, city):
        """Get all sites in a specific city"""
        matching_sites = [s for s in self.sites if s['City'].strip('"').lower() == city.lower()]
        
        if not matching_sites:
            return f"No sites found in city: {city}"
        
        result = f"Sites in {city} ({len(matching_sites)} found):\n\n"
        result += "ID | Class       | Type        | Status        | Address\n"
        result += "-" * 65 + "\n"
        
        for site in matching_sites:
            site_id = site['Id']
            pollution_class = site['PollutionClass'].strip('"')
            pollution_type = site['PollutionType'].strip('"')
            status = site['RemediationStatus'].strip('"')
            address = site['AddressLine'].strip('"')
            result += f"{site_id:2} | {pollution_class:11} | {pollution_type:11} | {status:13} | {address}\n"
        
        return result
    
    def format_site_details(self, site):
        """Format complete site details"""
        pollution_class = site['PollutionClass'].strip('"')
        pollution_type = site['PollutionType'].strip('"')
        status = site['RemediationStatus'].strip('"')
        start_date = site['RemediationStart'].strip('"')
        end_date = site['RemediationFinish'].strip('"')
        address = site['AddressLine'].strip('"')
        city = site['City'].strip('"')
        state = site['StateProvince'].strip('"')
        postal_code = site['PostalCode'].strip('"')
        country = site['Country'].strip('"')
        
        result = f"SuperFund Site Details:\n"
        result += f"  ID: {site['Id']}\n"
        result += f"  Pollution Class: {pollution_class}\n"
        result += f"  Pollution Type: {pollution_type}\n"
        result += f"  Remediation Status: {status}\n"
        
        if start_date:
            result += f"  Remediation Start: {start_date}\n"
        else:
            result += f"  Remediation Start: Not yet scheduled\n"
            
        if end_date:
            result += f"  Remediation Finish: {end_date}\n"
        else:
            result += f"  Remediation Finish: Not yet scheduled\n"
            
        result += f"  Location: {address}\n"
        result += f"  City: {city}, {state} {postal_code}\n"
        result += f"  Country: {country}\n"
        
        return result
    
    def show_help(self):
        """Show available superfundsite commands"""
        help_text = """
SuperFund Site Agent Commands:
- 'search site [ID]' - Get full details of a site
- 'site status [ID]' - Get remediation status of a specific site
- 'list sites' or 'show all sites' - List all sites
- 'count sites' - Show count of sites by category
- 'sites by pollution [type]' - Show sites with specific pollution type
- 'sites by class [class]' - Show sites with specific pollution class
- 'sites by status [status]' - Show sites with specific remediation status
- 'sites by city [city]' - Show all sites in a specific city
- 'evaluating sites' - Show sites currently being evaluated
- 'completed sites' - Show sites with completed remediation
- 'site help' - Show this help message

Examples:
- search site 5
- site status 10
- sites by pollution Nuclear
- sites by class Industrial
- sites by status In Progress
- sites by city Houston
- count sites
        """
        return help_text.strip()
