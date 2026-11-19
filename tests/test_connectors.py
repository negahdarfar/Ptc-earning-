from datetime import date

import pytest

from app.connectors import ConnectorManifest, ConnectorRegistry, ConnectorRegistrationError


def manifest(**overrides):
    values = {
        "connector_id": "sample",
        "display_name": "Sample Platform",
        "platform_url": "https://platform.example",
        "terms_url": "https://platform.example/terms",
        "api_base_url": "https://api.platform.example/v1",
        "official_api": True,
        "supported_countries": ("IR",),
        "payout_methods": ("crypto",),
        "rate_limit_per_minute": 30,
        "enabled": False,
        "terms_reviewed_on": date(2026, 11, 19),
        "review_note": "Primary terms reviewed; test fixture only.",
    }
    values.update(overrides)
    return ConnectorManifest(**values)


def test_connectors_are_disabled_by_default_and_not_recommended():
    registry = ConnectorRegistry()
    registry.register(manifest())
    assert registry.get("SAMPLE").enabled is False
    assert registry.list_for_country("IR") == []
    assert registry.list_for_country("IR", enabled_only=False) == [registry.get("sample")]


def test_enabled_connector_requires_explicit_iran_eligibility_and_review():
    registry = ConnectorRegistry()
    registry.register(manifest(enabled=True))
    assert [item.connector_id for item in registry.list_for_country("IR")] == ["sample"]

    with pytest.raises(ConnectorRegistrationError):
        ConnectorRegistry().register(manifest(enabled=True, supported_countries=("US",)))

    with pytest.raises(ConnectorRegistrationError):
        ConnectorRegistry().register(manifest(enabled=True, terms_reviewed_on=None))


def test_global_is_explicit_and_unknown_is_not_global():
    registry = ConnectorRegistry()
    registry.register(manifest(connector_id="global", supported_countries=("GLOBAL",)))
    registry.register(manifest(connector_id="unknown", supported_countries=("unknown",)))
    assert [item.connector_id for item in registry.list_for_country("IR", enabled_only=False)] == ["global"]


def test_enabled_connector_requires_official_https_api_and_rate_limit():
    for changes in (
        {"official_api": False},
        {"api_base_url": "http://api.example"},
        {"terms_url": "http://example/terms"},
        {"rate_limit_per_minute": 0},
    ):
        with pytest.raises(ConnectorRegistrationError):
            ConnectorRegistry().register(manifest(enabled=True, **changes))


def test_duplicate_connector_id_is_rejected():
    registry = ConnectorRegistry()
    registry.register(manifest())
    with pytest.raises(ConnectorRegistrationError):
        registry.register(manifest(display_name="Duplicate"))
