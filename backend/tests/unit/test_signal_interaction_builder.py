from core.analytics.signal_interaction_builder import build_signal_interactions_v1


def _map_payload():
    return {
        "map_version": "v1",
        "nodes": [
            {"signal_id": "signal_a"},
            {"signal_id": "signal_b"},
            {"signal_id": "signal_c"},
            {"signal_id": "signal_d"},
            {"signal_id": "signal_x"},
            {"signal_id": "signal_y"},
        ],
        "edges": [
            {
                "from_signal": "signal_a",
                "to_signal": "signal_b",
                "relationship_type": "driver",
                "evidence_strength": "strong",
                "rationale": "Signal A deterministically drives Signal B in this synthetic chain.",
            },
            {
                "from_signal": "signal_b",
                "to_signal": "signal_c",
                "relationship_type": "consequence",
                "evidence_strength": "moderate",
                "rationale": "Signal B deterministically contributes to Signal C continuation.",
            },
            {
                "from_signal": "signal_c",
                "to_signal": "signal_d",
                "relationship_type": "driver",
                "evidence_strength": "consensus",
                "rationale": "Signal C deterministically drives Signal D with strong evidence.",
            },
            {
                "from_signal": "signal_x",
                "to_signal": "signal_y",
                "relationship_type": "co_occurrence",
                "evidence_strength": "exploratory",
                "rationale": "Signals X and Y co-occur but remain isolated from the active test panel.",
            },
        ],
    }


def test_interaction_chains_are_deterministic_and_ranked():
    signal_results = [
        {"signal_id": "signal_a", "signal_state": "suboptimal"},
        {"signal_id": "signal_b", "signal_state": "at_risk"},
        {"signal_id": "signal_c", "signal_state": "suboptimal"},
        {"signal_id": "signal_d", "signal_state": "suboptimal"},
    ]
    out_one = build_signal_interactions_v1(signal_results=signal_results, map_payload=_map_payload())
    out_two = build_signal_interactions_v1(signal_results=signal_results, map_payload=_map_payload())

    assert out_one["interaction_graph"] == out_two["interaction_graph"]
    assert out_one["interaction_chains"] == out_two["interaction_chains"]
    assert out_one["interaction_summary"] == out_two["interaction_summary"]
    assert out_one["interaction_chains"] == [["signal_a", "signal_b", "signal_c", "signal_d"]]
    assert out_one["interaction_summary"][0]["priority_rank"] == 1
    assert out_one["interaction_summary"][0]["signals_involved"] == ["signal_a", "signal_b", "signal_c", "signal_d"]


def test_edge_isolation_for_absent_signals():
    signal_results = [
        {"signal_id": "signal_a", "signal_state": "suboptimal"},
        {"signal_id": "signal_b", "signal_state": "suboptimal"},
        {"signal_id": "signal_c", "signal_state": "suboptimal"},
        {"signal_id": "signal_d", "signal_state": "suboptimal"},
    ]
    output = build_signal_interactions_v1(signal_results=signal_results, map_payload=_map_payload())
    edges = output["interaction_graph"]["edges"]
    edge_pairs = {(edge["from_signal"], edge["to_signal"]) for edge in edges}
    assert ("signal_x", "signal_y") not in edge_pairs
    assert output["interaction_chains"] == [["signal_a", "signal_b", "signal_c", "signal_d"]]


def test_empty_when_no_mapped_edges_present():
    signal_results = [
        {"signal_id": "signal_a", "signal_state": "suboptimal"},
        {"signal_id": "signal_d", "signal_state": "at_risk"},
    ]
    output = build_signal_interactions_v1(signal_results=signal_results, map_payload=_map_payload())
    assert output["interaction_graph"]["nodes"] == ["signal_a", "signal_d"]
    assert output["interaction_graph"]["edges"] == []
    assert output["interaction_chains"] == []
    assert output["interaction_summary"] == []
