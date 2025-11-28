from dataclasses import dataclass

@dataclass
class Location:
    address: str
    city: str
    state_province: str
    postal_code: str
    country: str
    latitude: float
    longitude: float