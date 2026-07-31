# ARCH-CONV-E — ARCH-CONV-C manifest hash repair evidence

**Result:** `REPAIRED_METADATA_ONLY`  
**Commit:** `33e32a5` — `fix(governance): repair ARCH-CONV-C compiled manifest hashes`

## Defect

The two ARCH-CONV-C manifests contained stale `outputs[].output_hash` values.
The compiled artefacts themselves are byte-identical to their original
ARCH-CONV-C implementation and to the merged ARCH-CONV-C / ARCH-CONV-D
baselines.

| Asset | Stale manifest hash | Recomputed SHA-256 |
|---|---|---|
| `knowledge_bus/compiled/hypotheses/inv_alp_high_bone_biliary.yaml` | `387c4e5170cd34ae3bbb65b9cfd9a05eb2917698d262edaa8c38ab4e675db6d7` | `973f9a33581267a6fc7e1b5b87bda800840aa0f78588aa4dd931064374fd7633` |
| `knowledge_bus/compiled/hypotheses/inv_ggt_high_hepatic.yaml` | `55c7beaff048ecf849d389f9e9aee3a5dc8f3b72ede45ef4b5eddee8bdf2af16` | `d6b07d0202c8007a964ac9d4bac42e02438078972d46c668e697097f8d914f19` |

### Root cause

Independent recomputation shows the stale `output_hash` values are SHA-256 of
the **same compiled bytes after LF→CRLF conversion**, not different medical
content:

| Asset | LF (actual file / git blob) | CRLF (stale manifest) |
|---|---|---|
| ALP compiled | `973f9a33581267a6…fd7633` | `387c4e5170cd34ae…75db6d7` |
| GGT compiled | `d6b07d0202c8007a…914f19` | `55c7beaff048ecf8…df2af16` |

This is provenance-metadata drift only.

Note: `docs/architecture/ARCH-CONV-C_STOP_C_runtime_proof.md` still quotes the
pre-repair stale hashes. That is documentation drift only; runtime artefacts and
manifests on this branch now match the LF compiled bytes.

## Byte-preservation proof

For each compiled artefact, SHA-256 and byte length were recomputed from:

- current working-tree bytes;
- implementation commit `3dcfd39`;
- merged ARCH-CONV-C baseline `e2d7ce3`;
- ARCH-CONV-E baseline `39da186`.

Results:

| Asset | Bytes | Current | `3dcfd39` | `e2d7ce3` | `39da186` | Identical |
|---|---:|---|---|---|---|---|
| ALP compiled | 2446 | `973f9a…7633` | same | same | same | yes |
| GGT compiled | 2320 | `d6b07d…4f19` | same | same | same | yes |

Canonical source working-tree hashes remain the governed values already recorded
in the manifests:

- ALP source: `1a8e2da95d4aeae0505897da445709632f5ea4c39c34d4aaf906ef3462eb61ef`
- GGT source: `3e2cc6cf074dcb73b825e9a97fe93b43c4f50dc874a0c85cbaa34b754d46c8a1`

Historical Git blob byte hashes differ for the source YAMLs because the active
Windows checkout applies CRLF working-tree normalization. No source file was
edited by the repair.

## Change boundary

Only these fields changed:

```text
knowledge_bus/compiled/manifests/arch_conv_c_alp_high.yaml::outputs[0].output_hash
knowledge_bus/compiled/manifests/arch_conv_c_ggt_high.yaml::outputs[0].output_hash
```

No compiled artefact, canonical source, activation key, role, collision policy,
or medical content changed.

## Verification

```text
python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS; 37 frames, 21 compiled_active, 1 rejected, 15 legacy_retired

python -m pytest backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py -q
→ 20 passed
```
