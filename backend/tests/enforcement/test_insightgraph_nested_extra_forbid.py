"""
Sprint 8 enforcement: nested InsightGraph LayerC models forbid unknown fields.
"""

from pydantic import ValidationError

from core.contracts.insight_graph_v1 import (
    DetoxFeatureV1,
    FatigueFeatureV1,
    HeartFeatureV1,
    InflammationFeatureV1,
    InsightGraphV1,
    LayerCFeatureBundleV1,
    MetabolicAgeFeatureV1,
)


def test_metabolic_age_feature_forbids_extra_fields() -> None:
    MetabolicAgeFeatureV1()
    try:
        MetabolicAgeFeatureV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("MetabolicAgeFeatureV1 accepted unknown field")


def test_heart_feature_forbids_extra_fields() -> None:
    HeartFeatureV1()
    try:
        HeartFeatureV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("HeartFeatureV1 accepted unknown field")


def test_inflammation_feature_forbids_extra_fields() -> None:
    InflammationFeatureV1()
    try:
        InflammationFeatureV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("InflammationFeatureV1 accepted unknown field")


def test_fatigue_feature_forbids_extra_fields() -> None:
    FatigueFeatureV1()
    try:
        FatigueFeatureV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("FatigueFeatureV1 accepted unknown field")


def test_detox_feature_forbids_extra_fields() -> None:
    DetoxFeatureV1()
    try:
        DetoxFeatureV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("DetoxFeatureV1 accepted unknown field")


def test_layerc_bundle_forbids_extra_fields() -> None:
    LayerCFeatureBundleV1()
    try:
        LayerCFeatureBundleV1(unexpected_field=True)
    except ValidationError:
        return
    raise AssertionError("LayerCFeatureBundleV1 accepted unknown field")


def test_minimal_insightgraph_with_layerc_features_validates() -> None:
    bundle = LayerCFeatureBundleV1(
        metabolic_age=MetabolicAgeFeatureV1(),
        heart_insight=HeartFeatureV1(),
        inflammation=InflammationFeatureV1(),
        fatigue_root_cause=FatigueFeatureV1(),
        detox_filtration=DetoxFeatureV1(),
    )
    graph = InsightGraphV1(layer_c_features=bundle)
    assert graph.layer_c_features is not None
