from dataclasses import dataclass
import datetime
from typing import Optional  # Fixed: import Optional from typing module
from .Location import Location


@dataclass
class LocationScoringRequest:
    """Request object for location scoring"""
    location: Location
    radius_miles: float # Search radius in miles for nearby superfund sites - should default to 50 but be overridable

