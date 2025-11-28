from dataclasses import dataclass
import datetime
from typing import Optional  # Fixed: import Optional from typing module
from .Location import Location

@dataclass
class Policy:
    policy_number: str
    policy_type: str
    effective_date: datetime.datetime
    expiration_date: datetime.datetime
    location: Location
    status: str
    endorsement_amount: float