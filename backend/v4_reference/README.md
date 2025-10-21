# V4 Reference Files (Read-Only)

**Purpose:** Archived v4 reference files for read-only inspection only during the Canonization & Validation Refactor (v4 → v5 Integration).

## File Manifest

- `biomarker_alias_registry.py` - Python module for loading and accessing biomarker alias mappings from YAML
- `biomarker_alias_registry.yaml` - YAML configuration containing canonical biomarker IDs and their aliases
- `biomarker_aliases.py` - Additional biomarker alias utilities and helper functions
- `biomarkerAliases.ts` - TypeScript service for client-side biomarker alias resolution and validation
- `biomarkers_config.yaml` - Biomarker configuration file with ranges and validation rules
- `context_factory.py` - ContextFactory class for creating validated AnalysisContext objects from raw data

## ⚠️ Important Warning

**Do NOT import these modules directly from runtime code.** These files are provided for reference only during the refactor process. They will be used to inform the implementation of new v5 canonicalization logic but should not be integrated directly into the active codebase.

## Usage

These files serve as reference material for:
- Understanding v4 canonicalization patterns
- Porting mature validation logic to v5
- Maintaining consistency with established biomarker handling
- Ensuring backward compatibility during the transition

Last updated: Sprint 0 - Preparation & Baseline
