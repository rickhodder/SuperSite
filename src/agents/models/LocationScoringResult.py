from dataclasses import dataclass
from .LocationScoringRequest import LocationScoringRequest
from .SuperFundSite import SuperFundSite


@dataclass
class LocationScoringResult:
    """Result object for location scoring"""
    request: LocationScoringRequest # original request
    nearby_superfund_sites: list[SuperFundSite]


