"""Official, policy-checked platform connector framework."""

from .base import ConnectorManifest, OpportunityCandidate
from .registry import ConnectorRegistry, ConnectorRegistrationError

__all__ = [
    "ConnectorManifest",
    "OpportunityCandidate",
    "ConnectorRegistry",
    "ConnectorRegistrationError",
]
