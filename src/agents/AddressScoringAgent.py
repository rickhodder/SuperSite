import csv
import os
import math
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .BaseAgent import BaseAgent
from .models.Location import Location
from .models.SuperFundSite import SuperFundSite

class AddressScoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Address Scoring Agent")
        self.csv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'superfundsites.csv')
        self.superfund_sites = []
        self.load_superfund_sites()
    
    def load_superfund_sites(self):
        """Load superfund sites from CSV file and convert to SuperFundSite objects"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.superfund_sites = []
                
                for row in reader:
                    # Create Location object
                    location = Location(
                        address=row['AddressLine'].strip('"'),
                        city=row['City'].strip('"'),
                        state_province=row['StateProvince'].strip('"'),
                        postal_code=row['PostalCode'].strip('"'),
                        country=row['Country'].strip('"'),
                        latitude=0.0,  # Default value - could be geocoded later
                        longitude=0.0  # Default value - could be geocoded later
                    )
                    
                    # Parse dates if they exist
                    remediation_start = None
                    remediation_finish = None
                    
                    start_date_str = row['RemediationStart'].strip('"')
                    finish_date_str = row['RemediationFinish'].strip('"')
                    
                    if start_date_str:  # If not empty
                        try:
                            remediation_start = datetime.strptime(start_date_str, '%Y-%m-%d')
                        except ValueError:
                            remediation_start = None
                    
                    if finish_date_str:  # If not empty
                        try:
                            remediation_finish = datetime.strptime(finish_date_str, '%Y-%m-%d')
                        except ValueError:
                            remediation_finish = None
                    
                    # Create SuperFundSite object
                    superfund_site = SuperFundSite(
                        location=location,
                        pollution_class=row['PollutionClass'].strip('"'),
                        pollution_type=row['PollutionType'].strip('"'),
                        remediation_status=row['RemediationStatus'].strip('"'),
                        remediation_start=remediation_start,
                        remediation_finish=remediation_finish,
                        distance_miles=0.0  # Will be calculated during evaluation
                    )
                    
                    self.superfund_sites.append(superfund_site)
            
            print(f"Loaded {len(self.superfund_sites)} SuperFundSite objects for address evaluation")
        except FileNotFoundError:
            print(f"SuperFund sites CSV file not found at: {self.csv_file}")
            self.superfund_sites = []
        except Exception as e:
            print(f"Error loading superfund sites for address evaluation: {e}")
            self.superfund_sites = []
    
    def get_coordinates_from_postal_code(self, postal_code: str) -> Optional[Tuple[float, float]]:
        """
        Get approximate coordinates from postal code
        This is a simplified mapping for demo purposes
        In production, you would use a proper geocoding API
        """
        # Sample postal code to coordinates mapping for major US cities
        postal_coords = {
            # New York area
            "10001": (40.7505, -73.9934), "10002": (40.7156, -73.9877), "10003": (40.7310, -73.9896),
            "10004": (40.7047, -74.0142), "10005": (40.7056, -74.0088), "10006": (40.7089, -74.0132),
            
            # California area
            "90210": (34.0901, -118.4065), "90211": (34.0836, -118.4089), "90212": (34.1030, -118.4104),
            "90301": (34.0194, -118.3957), "92101": (32.7157, -117.1611), "94102": (37.7849, -122.4094),
            
            # Illinois area
            "60601": (41.8827, -87.6233), "60602": (41.8819, -87.6278), "60603": (41.8781, -87.6298),
            "60604": (41.8781, -87.6298), "60605": (41.8683, -87.6201), "60606": (41.8847, -87.6441),
            
            # Texas area
            "77001": (29.7589, -95.3677), "77002": (29.7633, -95.3633), "77003": (29.7441, -95.3370),
            "77004": (29.7411, -95.3844), "77005": (29.7199, -95.4009), "77006": (29.7604, -95.3697),
            
            # Arizona area
            "85001": (33.4734, -112.0740), "85002": (33.4734, -112.0740), "85003": (33.4484, -112.0740),
            "85004": (33.4734, -112.0585), "85005": (33.4256, -112.1168), "85006": (33.4734, -112.0323),
            
            # Pennsylvania area
            "19101": (39.9526, -75.1652), "19102": (39.9526, -75.1652), "19103": (39.9526, -75.1652),
            
            # Florida area
            "33101": (25.7617, -80.1918), "33102": (25.7617, -80.1918), "33103": (25.7617, -80.1918),
            
            # Additional major cities
            "30301": (33.7490, -84.3880), # Atlanta, GA
            "98101": (47.6062, -122.3321), # Seattle, WA
            "80201": (39.7392, -104.9903), # Denver, CO
            "48201": (42.3314, -83.0458), # Detroit, MI
            "21201": (39.2904, -76.6122), # Baltimore, MD
            "53201": (43.0389, -87.9065), # Milwaukee, WI
            "87101": (35.0844, -106.6504), # Albuquerque, NM
            "85701": (32.2217, -110.9265), # Tucson, AZ
            "93701": (36.7378, -119.7871), # Fresno, CA
            "95801": (38.5816, -121.4944), # Sacramento, CA
            "64101": (39.0997, -94.5786), # Kansas City, MO
            "85201": (33.4152, -111.8315), # Mesa, AZ
            "23451": (36.8529, -75.9780), # Virginia Beach, VA
            "80901": (38.8339, -104.8214), # Colorado Springs, CO
            "68101": (41.2565, -95.9345), # Omaha, NE
            "27601": (35.7796, -78.6382), # Raleigh, NC
            "55401": (44.9778, -93.2650), # Minneapolis, MN
            "74101": (36.1540, -95.9928), # Tulsa, OK
            "44101": (41.4993, -81.6944), # Cleveland, OH
            "67201": (37.6872, -97.3301), # Wichita, KS
        }
        
        return postal_coords.get(postal_code)
    
    def extract_postal_code(self, address: str) -> Optional[str]:
        """Extract postal code from address string"""
        # Look for 5-digit postal code
        postal_match = re.search(r'\b(\d{5})\b', address)
        if postal_match:
            return postal_match.group(1)
        return None
    
    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in miles
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in miles
        r = 3956
        
        return c * r
    
    def get_site_coordinates(self, site: SuperFundSite) -> Optional[Tuple[float, float]]:
        """Get coordinates for a superfund site based on its postal code"""
        postal_code = site.location.postal_code
        return self.get_coordinates_from_postal_code(postal_code)
    
    def evaluate_address_safety(self, address: str) -> Dict:
        """
        Evaluate address safety based on proximity to superfund sites
        Returns a dict with score and nearby sites as per specification
        """
        # Extract postal code from address
        postal_code = self.extract_postal_code(address)
        
        if not postal_code:
            return {
                "score": 0.0,
                "nearby_sites": [],
                "error": "Could not extract postal code from address. Please include a valid 5-digit postal code.",
                "address": address
            }
        
        # Get coordinates for input address
        input_coords = self.get_coordinates_from_postal_code(postal_code)
        
        if not input_coords:
            return {
                "score": 0.0,
                "nearby_sites": [],
                "error": f"Unknown postal code: {postal_code}. Please use a supported postal code.",
                "address": address
            }
        
        nearby_sites = []
        
        # Check each superfund site for proximity
        for site in self.superfund_sites:
            site_coords = self.get_site_coordinates(site)
            
            if site_coords:
                distance = self.calculate_distance(input_coords, site_coords)
                
                if distance <= 50:  # Within 50 miles
                    # Create a new SuperFundSite object with calculated distance
                    nearby_site = SuperFundSite(
                        location=site.location,
                        pollution_class=site.pollution_class,
                        pollution_type=site.pollution_type,
                        remediation_status=site.remediation_status,
                        remediation_start=site.remediation_start,
                        remediation_finish=site.remediation_finish,
                        distance_miles=round(distance, 2)
                    )
                    nearby_sites.append(nearby_site)
        
        # Calculate safety score according to specification:
        # - Start with 1.0 (100% safe)
        # - Reduce by 0.25 for each nearby site
        # - Never go below 0.0 (0% safe)
        if len(nearby_sites) == 0:
            score = 1.0  # 100% safe - no nearby sites
        else:
            score = max(0.0, 1.0 - (len(nearby_sites) * 0.25))
        
        return {
            "score": score,
            "nearby_sites": nearby_sites
        }
    
    def process_input(self, user_input: str) -> str:
        """Process user input and return address safety evaluation"""
        user_input_lower = user_input.lower()
        
        if "help" in user_input_lower or "address help" in user_input_lower:
            return self.show_help()
        
        elif user_input_lower.startswith("evaluate") or user_input_lower.startswith("score"):
            # Extract address from command
            parts = user_input.split(" ", 1)
            if len(parts) >= 2:
                address = parts[1]
                result = self.evaluate_address_safety(address)
                return self.format_evaluation_result(result)
            else:
                return "Please provide an address to evaluate. Example: 'evaluate 123 Main St, New York, NY 10001'"
        
        elif "safety" in user_input_lower:
            # Extract address from after "safety"
            safety_index = user_input_lower.find("safety")
            if safety_index != -1:
                address = user_input[safety_index + 6:].strip()
                if address:
                    result = self.evaluate_address_safety(address)
                    return self.format_evaluation_result(result)
            return "Please provide an address after 'safety'. Example: 'safety 123 Main St, New York, NY 10001'"
        
        elif any(char.isdigit() for char in user_input):
            # If input contains digits, treat as address
            result = self.evaluate_address_safety(user_input)
            return self.format_evaluation_result(result)
        
        else:
            return "I can evaluate address safety based on nearby superfund sites. Try 'evaluate [address]' or 'help' for more commands."
    
    def process_task(self, task):
        """Process a specific address safety evaluation task"""
        return self.process_input(task)
    
    def format_evaluation_result(self, result: Dict) -> str:
        """Format the evaluation result for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        score = result['score']
        nearby_sites = result['nearby_sites']
        sites_count = len(nearby_sites)
        percentage = f"{score * 100:.1f}%"
        
        # Determine safety level based on score
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
        
        # Build response
        response = f"{emoji} SAFETY SCORE: {percentage} - {safety_level}\n"
        response += f"Superfund sites within 50 miles: {sites_count}\n"
        
        if sites_count > 0:
            response += f"\n📍 NEARBY SUPERFUND SITES:\n"
            for i, site in enumerate(nearby_sites, 1):
                response += f"{i}. {site.pollution_class} Site ({site.distance_miles} miles)\n"
                response += f"   📍 {site.location.address}, {site.location.city}, {site.location.state_province}\n"
                response += f"   🏭 {site.pollution_class} - {site.pollution_type}\n"
                response += f"   🔧 Status: {site.remediation_status}\n"
                
                # Add date information if available
                if site.remediation_start:
                    response += f"   📅 Start: {site.remediation_start.strftime('%Y-%m-%d')}\n"
                if site.remediation_finish:
                    response += f"   📅 Finish: {site.remediation_finish.strftime('%Y-%m-%d')}\n"
                response += "\n"
        else:
            response += "\n✅ No superfund sites found within 50 miles!"
        
        return response.strip()
    
    def show_help(self):
        """Show available address scoring commands"""
        help_text = """
Address Scoring Agent Commands:
- 'evaluate [address]' - Evaluate safety score for an address
- 'score [address]' - Same as evaluate
- 'safety [address]' - Check safety of an address
- '[address with postal code]' - Direct address input

Scoring Rules:
- Starts at 1.0 (100% safe)
- Reduces by 0.25 for each superfund site within 50 miles
- Minimum score is 0.0 (0% safe)

Examples:
- evaluate 123 Main St, New York, NY 10001
- safety Los Angeles, CA 90210
- score Houston, TX 77001
- 456 Oak Ave, Chicago, IL 60601

Note: Address must include a valid postal code for evaluation.
        """
        return help_text.strip()
