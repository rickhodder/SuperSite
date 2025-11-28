from dataclasses import dataclass
import datetime
from typing import Optional  # Fixed: import Optional from typing module
from .Location import Location


# does epa have severity ratings for superfund sites?   
@dataclass
class SuperFundSite:
    """Superfund site object with location and contamination details"""
    site_name: str
    location: Location
    pollution_class: str
    pollution_type: str
    remediation_status: str
    remediation_start: Optional[datetime.datetime]
    remediation_finish: Optional[datetime.datetime]
    distance_miles: float