from core.canonical.alias_registry_service import AliasRegistryService, get_alias_registry_service


def test_uric_acid_alias_resolves_to_urate(monkeypatch):
    get_alias_registry_service.cache_clear()
    monkeypatch.setattr(
        AliasRegistryService,
        "_add_common_aliases",
        lambda self, alias_mapping, insert_alias: None,
    )
    resolver = get_alias_registry_service()
    assert resolver.resolve("uric_acid") == "urate"
    assert resolver.resolve("urate") == "urate"
    get_alias_registry_service.cache_clear()
