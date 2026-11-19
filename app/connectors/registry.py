from .base import ConnectorManifest


class ConnectorRegistrationError(ValueError):
    pass


class ConnectorRegistry:
    """In-memory registry; it performs no network calls or account actions."""

    def __init__(self) -> None:
        self._connectors: dict[str, ConnectorManifest] = {}

    def register(self, manifest: ConnectorManifest) -> None:
        key = manifest.connector_id.strip().lower()
        if not key or key in self._connectors:
            raise ConnectorRegistrationError("connector_id must be unique and non-empty")
        if manifest.rate_limit_per_minute < 0:
            raise ConnectorRegistrationError("rate_limit_per_minute cannot be negative")
        if manifest.enabled and not manifest.is_enableable():
            raise ConnectorRegistrationError(
                "enabled connectors must have an official HTTPS API, reviewed HTTPS terms, "
                "a positive rate limit, and an explicit supported-country declaration"
            )
        self._connectors[key] = manifest

    def get(self, connector_id: str) -> ConnectorManifest | None:
        return self._connectors.get(connector_id.strip().lower())

    def list_for_country(self, country: str, enabled_only: bool = True) -> list[ConnectorManifest]:
        code = country.strip().upper()
        results = [
            item for item in self._connectors.values()
            if item.supports_country(code)
            and (not enabled_only or item.enabled)
            and item.is_reviewable_for(code)
        ]
        return sorted(results, key=lambda item: item.display_name.casefold())

    def __len__(self) -> int:
        return len(self._connectors)
