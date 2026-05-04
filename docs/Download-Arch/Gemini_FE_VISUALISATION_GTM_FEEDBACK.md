# FE-VISUALISATION Strategy & Feedback: HealthIQ Phase 3

## 1. Component Specific Recommendations

### BiomarkerChart
*   **Purpose:** The atomic unit of data trust.
*   **Standard Surface:** Raw value, units, and a visual "needle" on the lab-specific range.
*   **Advanced Mode:** Surface the **Lab-Anchored Z-Score**. This allows clinicians to see exactly how many "widths" a marker is from the center, providing a mathematical sense of urgency[cite: 4].
*   **Never Imply:** Do not imply a "Diagnosis." The chart shows a state, not a disease.

### ClusterCard
*   **Purpose:** Surface the "Quantified Magnitude" from the Sprint 13 Burden Engine.
*   **Standard Surface:** The **System Capacity Score** (e.g., "Metabolic Resilience: 84/100"). Use a "Gage" visualization[cite: 4].
*   **Advanced Mode:** List the "Top Burden Drivers" (e.g., "Driven by: Glucose Z: +2.1")[cite: 4].
*   **Internal/Debug:** Raw `adjusted_system_burden_vector` and BFS distance damping factors[cite: 4].

### InsightPanel
*   **Purpose:** The "Lead Domino" narrator.
*   **Standard Surface:** The **Primary Driver** narrative. For the current patient, this MUST lead with the **Methylation/Homocysteine** block[cite: 4].
*   **Advanced Mode:** Surface "Ranked Ambiguity"—show the secondary hypothesis (e.g., "Secondary stress detected in Renal filtration")[cite: 4].
*   **Handcuff Rule:** This component must be programmatically blocked from mentioning any system not identified as a `driver` or `supporting` system in the Arbitration Report[cite: 4].

### Data Integrity (formerly PipelineStatus)
*   **Purpose:** Contextualize the "Reliability" of the results.
*   **Standard Surface:** "Analysis verified against Lab-Specific Ranges. High confidence in Cardiovascular insights."
*   **Internal/Debug:** Hash verification status (`burden_hash` vs `replay_manifest`)[cite: 4].

## 2. The Surface-Policy Framework

| Layer | Target User | Focus |
| :--- | :--- | :--- |
| **Standard** | Retail End User | "Capacity" (0-100), "Primary Driver" narrative, and simple Range Charts[cite: 4]. |
| **Advanced** | Clinician / Optimizer | Z-Scores, Adjusted Burden Vectors, and Ranked Ambiguities[cite: 4]. |
| **Internal** | Engineering / QA | BFS Graph Distances, Replay Hashes, and raw JSON payloads[cite: 4]. |

## 3. Discussion Questions for Sprint Implementation
1. Does the `ClusterCard` successfully invert "Burden" to "Capacity" for the user?
2. Are we successfully hiding the `risk_direction` logic while showing its effect?
3. Can the `InsightPanel` handle a "Negative Result" (e.g., explaining why ApoB means the user shouldn't worry about Cholesterol)?[cite: 4]