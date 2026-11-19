from dataclasses import dataclass, field
from datetime import date
from typing import Protocol, Sequence


@dataclass(frozen=True)
class ConnectorManifest:
    """Auditable metadata for one official platform integration.

    Connectors are disabled by default. A connector is eligible only when its
    official API and current terms have been reviewed for the operator country.
    """

    connector_id: str
    display_name: str
    platform_url: str
    terms_url: str
    api_base_url: str
    official_api: bool
    supported_countries: tuple[str, ...] = field(default_factory=tuple)
    payout_methods: tuple[str, ...] = field(default_factory=tuple)
    rate_limit_per_minute: int = 0
    enabled: bool = False
    terms_reviewed_on: date | None = None
    review_note: str = ""

    def normalized_countries(self) -> set[str]:
        return {country.strip().upper() for country in self.supported_countries}

    def supports_country(self, country: str) -> bool:
        code = country.strip().upper()
        allowed = self.normalized_countries()
        return code in allowed or "GLOBAL" in allowed

    def is_reviewable_for(self, country: str) -> bool:
        return bool(
            self.official_api
            and self.terms_url.startswith("https://")
            and self.api_base_url.startswith("https://")
            and self.terms_reviewed_on is not None
            and self.supports_country(country)
            and self.rate_limit_per_minute > 0
        )


@dataclass(frozen=True)
class OpportunityCandidate:
    """Untrusted data returned by a connector; never auto-approved."""

    name: str
    category: str
    platform_url: str
    country_eligibility: str = "unknown"
    payout_method: str = "unknown"
    evidence_url: str = ""
    notes: str = ""


class OfficialPlatformConnector(Protocol):
    manifest: ConnectorManifest

    async def fetch_candidates(self, country: str) -> Sequence[OpportunityCandidate]:
        """Fetch candidates through the platform's documented official API."""
        ...
