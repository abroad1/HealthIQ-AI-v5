# 🧠 HealthIQ-AI v5 - Modular Insights Engine Refactor Plan

> **Sprint 9c-10: Complete Modular Insights Architecture Implementation**

---

## 📋 **Executive Summary**

### **What Changes**
Transform the current category-based insight synthesis system into a modular, versioned, manifest-driven insights engine with full provenance tracking. Replace hard-coded categories (`metabolic`, `cardiovascular`, `inflammatory`) with plug-and-play insight modules that can be versioned, A/B tested, and audited.

**Insight ID Policy**: Use lowercase snake_case format (e.g., `metabolic_age`, `heart_insight`), immutable once released. Versions use SemVer (`v1.2.0`). Enforce via validator.

All insight IDs and versions must also be documented in a central reference file (`docs/insights_registry.md`) to prevent duplication and to provide a single source of truth.

### **Why This Matters**
- **Business Agility**: Add/remove insights without code changes
- **Experimentation**: A/B test insight variants safely
- **Auditability**: Track which insights generated which results
- **Versioning**: Support insight evolution over time
- **Maintainability**: Clean separation of concerns
- **Determinism**: Stable, predictable insight execution order
- **Error Resilience**: Structured failure handling prevents pipeline aborts

### **Expected Outcomes**
- **Modular Architecture**: 5+ concrete insight modules with versioning
- **Manifest-Driven**: JSON configuration controls active insights
- **Full Provenance**: Track `manifest_id`, `insight_id`, `version`, `experiment_id`
- **Zero Downtime**: Clean replacement of category system
- **Test Coverage**: 100% pass rate on new modular system

### **Key Risks & Mitigations**
- **Test Churn**: 20+ tests reference categories → Comprehensive test migration plan
- **Frontend Compatibility**: DTO changes → Maintain backward-compatible DTO structure
- **Migration Complexity**: Database schema changes → Incremental migration with rollback
- **Performance Impact**: Sequential execution → Future parallelization ready

---

## 🏗️ **Architecture Target**

### **Enhanced BaseInsight Contract**
```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

@dataclass
class InsightMetadata:
    insight_id: str  # lowercase snake_case, immutable once released
    version: str     # SemVer format (v1.2.0)
    category: str
    required_biomarkers: List[str]
    optional_biomarkers: List[str] = None
    description: str
    author: str
    created_at: str
    updated_at: str

@dataclass
class InsightResult:
    insight_id: str
    version: str
    manifest_id: str
    result_key: Optional[str] = None  # For sub-insights to avoid overwrites
    drivers: Dict[str, Any] = None    # Standardized drivers JSONB
    evidence: Dict[str, Any] = None   # Standardized evidence JSONB
    biomarkers_involved: List[str] = None
    confidence: float = None
    severity: str = None
    error_code: Optional[str] = None
    error_detail: Optional[str] = None

class BaseInsight(ABC):
    @property
    @abstractmethod
    def metadata(self) -> InsightMetadata:
        pass
    
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        pass
    
    def can_analyze(self, context: AnalysisContext) -> bool:
        required = set(self.metadata.required_biomarkers)
        available = set(context.biomarker_panel.biomarkers.keys())
        return required.issubset(available)

**Contract Rule**: All insights must consume only `AnalysisContext`. Legacy `ScoredContext` is fully deprecated and unsupported.
```

### **Versioned Registry System**
```python
def register_insight(insight_id: str, version: str):
    def decorator(cls):
        registry.register(insight_id, version, cls)
        return cls
    return decorator

class InsightRegistry:
    def register(self, insight_id: str, version: str, insight_class: Type[BaseInsight])
    def get(self, insight_id: str, version: str) -> BaseInsight
    def get_all(self) -> List[BaseInsight]
    def list_versions(self, insight_id: str) -> List[str]
    def ensure_insights_registered(self) -> None  # Explicit import trigger
    def assert_registered(self, insight_id: str, version: str) -> None  # Boot validation
```

### **Manifest System**
```python
@dataclass
class InsightManifest:
    schema_version: str
    manifest_id: str
    name: str
    description: str
    created_by: str
    updated_by: str
    insights: List[InsightConfig]
    overrides: Optional[Dict[str, Any]] = None

@dataclass
class InsightConfig:
    insight_id: str
    version: str
    enabled: bool
    weight: float = 1.0

class ManifestService:
    def get_active_manifest(self) -> InsightManifest
    def get_enabled_insights(self) -> List[InsightConfig]
    def validate_manifest(self, manifest: Dict) -> bool
    def validate_insight_registry(self) -> None  # Fail fast if (id,version) missing
```

### **Orchestrator Integration**
```python
# Pseudocode for manifest-driven dispatch
def synthesize_insights(self, context: AnalysisContext) -> Dict[str, Any]:
    manifest = self.manifest_service.get_active_manifest()
    insights = []
    timing_metrics = {}
    
    # Process insights in stable manifest order
    for config in manifest.insights:
        if config.enabled:
            start_time = time.time()
            try:
                insight_module = self.registry.get(config.insight_id, config.version)
                if insight_module.can_analyze(context):
                    results = insight_module.analyze(context)
                    
                    # Add provenance metadata in-memory
                    for result in results:
                        result.insight_id = config.insight_id
                        result.version = config.version
                        result.manifest_id = manifest.manifest_id
                        result.experiment_id = getattr(config, 'experiment_id', None)
                    
                    insights.extend(results)
                    
            except Exception as e:
                # Structured failure - never abort pipeline
                error_result = InsightResult(
                    insight_id=config.insight_id,
                    version=config.version,
                    manifest_id=manifest.manifest_id,
                    error_code="ANALYSIS_FAILED",
                    error_detail=str(e)
                )
                insights.append(error_result)
            
            # Record timing metrics
            timing_metrics[config.insight_id] = int((time.time() - start_time) * 1000)
    
    # Sort by manifest order, then insight_id for stable output
    # Final insight results must be ordered strictly by manifest order; insight_id is only used for tie-breaking
    insights.sort(key=lambda x: (manifest.insights.index(next(c for c in manifest.insights if c.insight_id == x.insight_id)), x.insight_id))
    
    return self._build_response(insights, timing_metrics)
```

### **Database Provenance Schema**
```sql
-- Enhanced insights table
ALTER TABLE insights ADD COLUMN insight_id VARCHAR(100) NOT NULL;
ALTER TABLE insights ADD COLUMN version VARCHAR(20) NOT NULL;
ALTER TABLE insights ADD COLUMN manifest_id VARCHAR(100) NOT NULL;
ALTER TABLE insights ADD COLUMN experiment_id VARCHAR(100) NULL;
ALTER TABLE insights ADD COLUMN drivers JSONB;
ALTER TABLE insights ADD COLUMN evidence JSONB;
ALTER TABLE insights ADD COLUMN error_code VARCHAR(50);
ALTER TABLE insights ADD COLUMN error_detail TEXT;
ALTER TABLE insights ADD COLUMN latency_ms INTEGER NOT NULL DEFAULT 0;

-- After backfilling defaults, drop server_default
ALTER TABLE insights ALTER COLUMN insight_id DROP DEFAULT;
ALTER TABLE insights ALTER COLUMN version DROP DEFAULT;
ALTER TABLE insights ALTER COLUMN manifest_id DROP DEFAULT;

-- New indexes
CREATE UNIQUE INDEX idx_insights_unique_analysis_insight_version ON insights(analysis_id, insight_id, version);
CREATE INDEX idx_insights_insight_id_version ON insights(insight_id, version);
CREATE INDEX idx_insights_manifest_id ON insights(manifest_id);
CREATE INDEX idx_insights_drivers_gin ON insights USING GIN (drivers);
CREATE INDEX idx_insights_evidence_gin ON insights USING GIN (evidence);

-- Keep legacy category nullable for one sprint
ALTER TABLE insights ALTER COLUMN category DROP NOT NULL;
```

---

## 🚀 **Sprints and Scope**

### **Sprint 9c — Foundation (2 weeks)**

#### **Definition of Ready**
- [ ] Current architecture audited and blockers identified
- [ ] Database migration strategy confirmed
- [ ] Test migration plan created
- [ ] Frontend compatibility verified

#### **Definition of Done**
- [ ] Enhanced BaseInsight contract implemented
- [ ] Versioned registry with duplicate prevention
- [ ] Manifest service with JSON validation
- [ ] Database migration applied successfully
- [ ] All new unit tests passing
- [ ] DTOs include provenance fields

#### **Acceptance Criteria**
- [ ] Registry prevents duplicate (insight_id, version) pairs
- [ ] Manifest validates against JSON schema
- [ ] Database migration runs without data loss
- [ ] DTOs include `insight_id`, `version`, `manifest_id` fields
- [ ] `category` field must still be populated from `metadata.category` until Sprint 10a for frontend compatibility
- [ ] 100% pass rate on new unit tests

#### **Files to Create/Modify**

**New Files:**
- `backend/core/insights/metadata.py` - InsightMetadata dataclass
- `backend/services/insights/manifest_service.py` - Manifest management
- `backend/data/insight_manifests/default.json` - Default manifest
- `backend/data/insight_manifests/manifest.schema.json` - JSON schema
- `backend/migrations/versions/XXXXXXXX_insight_provenance.py` - Alembic migration

**Modified Files:**
- `backend/core/insights/base.py` - Enhanced BaseInsight contract
- `backend/core/insights/registry.py` - Version-aware registry
- `backend/core/models/database.py` - Add provenance fields to insights table
- `backend/core/dto/builders.py` - Include provenance in DTOs

#### **Manifest JSON Schema**
```json
{
  "schema_version": "1.0",
  "manifest_id": "production_v1",
  "name": "Production Insights Manifest",
  "description": "Default production insight configuration",
  "created_by": "HealthIQ Team",
  "updated_by": "HealthIQ Team",
  "insights": [
    {
      "insight_id": "metabolic_age",
      "version": "v1.0.0",
      "enabled": true,
      "weight": 1.0
    },
    {
      "insight_id": "heart_insight", 
      "version": "v1.0.0",
      "enabled": true,
      "weight": 1.0
    },
    {
      "insight_id": "inflammation",
      "version": "v1.0.0", 
      "enabled": true,
      "weight": 1.0
    },
    {
      "insight_id": "fatigue_root_cause",
      "version": "v1.0.0",
      "enabled": true,
      "weight": 1.0
    },
    {
      "insight_id": "detox_filtration",
      "version": "v1.0.0",
      "enabled": true,
      "weight": 1.0
    }
  ]
}
```

#### **Alembic Migration**
```python
def upgrade():
    # Add provenance columns with defaults
    op.add_column('insights', sa.Column('insight_id', sa.String(100), nullable=False, server_default='legacy'))
    op.add_column('insights', sa.Column('version', sa.String(20), nullable=False, server_default='v1.0.0'))
    op.add_column('insights', sa.Column('manifest_id', sa.String(100), nullable=False, server_default='legacy_v1'))
    op.add_column('insights', sa.Column('experiment_id', sa.String(100), nullable=True))
    op.add_column('insights', sa.Column('drivers', sa.JSON(), nullable=True))
    op.add_column('insights', sa.Column('evidence', sa.JSON(), nullable=True))
    op.add_column('insights', sa.Column('error_code', sa.String(50), nullable=True))
    op.add_column('insights', sa.Column('error_detail', sa.Text(), nullable=True))
    op.add_column('insights', sa.Column('latency_ms', sa.Integer(), nullable=True))
    
    # Update existing records
    op.execute("UPDATE insights SET insight_id = 'legacy_' || category, manifest_id = 'legacy_v1'")
    
    # Drop server defaults after backfilling
    op.alter_column('insights', 'insight_id', server_default=None)
    op.alter_column('insights', 'version', server_default=None)
    op.alter_column('insights', 'manifest_id', server_default=None)
    
    # Add indexes
    op.create_unique_index('idx_insights_unique_analysis_insight_version', 'insights', ['analysis_id', 'insight_id', 'version'])
    op.create_index('idx_insights_insight_id_version', 'insights', ['insight_id', 'version'])
    op.create_index('idx_insights_manifest_id', 'insights', ['manifest_id'])
    op.create_index('idx_insights_drivers_gin', 'insights', ['drivers'], postgresql_using='gin')
    op.create_index('idx_insights_evidence_gin', 'insights', ['evidence'], postgresql_using='gin')
    
    # Make category nullable for one sprint
    op.alter_column('insights', 'category', nullable=True)

def downgrade():
    op.drop_index('idx_insights_evidence_gin', 'insights')
    op.drop_index('idx_insights_drivers_gin', 'insights')
    op.drop_index('idx_insights_manifest_id', 'insights')
    op.drop_index('idx_insights_insight_id_version', 'insights')
    op.drop_index('idx_insights_unique_analysis_insight_version', 'insights')
    op.drop_column('insights', 'latency_ms')
    op.drop_column('insights', 'error_detail')
    op.drop_column('insights', 'error_code')
    op.drop_column('insights', 'evidence')
    op.drop_column('insights', 'drivers')
    op.drop_column('insights', 'experiment_id')
    op.drop_column('insights', 'manifest_id')
    op.drop_column('insights', 'version')
    op.drop_column('insights', 'insight_id')
    op.alter_column('insights', 'category', nullable=False)
```

#### **Tests to Implement**
- **Unit Tests**: Registry registration/retrieval, manifest validation, DTO provenance
- **Migration Tests**: Forward/backward migration smoke tests
- **Integration Tests**: Manifest service with database

---

### **Sprint 9d — Concrete Modules v1 (2 weeks)**

#### **Definition of Ready**
- [ ] Sprint 9c foundation complete
- [ ] Registry and manifest system stable
- [ ] Database migration applied

#### **Definition of Done**
- [ ] 5 concrete insight modules implemented
- [ ] All modules auto-register via decorators
- [ ] Each module passes unit tests
- [ ] Modules integrate with registry
- [ ] Golden output tests for deterministic modules

#### **Acceptance Criteria**
- [ ] All 5 modules load via registry
- [ ] Each module implements required metadata
- [ ] `can_analyze()` works correctly for each module
- [ ] Modules generate valid Insight objects
- [ ] Golden parity with v4 outputs must be achieved within ±1% tolerance on fixture panels
- [ ] 100% pass rate on module unit tests

#### **Files to Create**

**Module Files:**
- `backend/core/insights/modules/metabolic_age.py`
- `backend/core/insights/modules/heart_insight.py`
- `backend/core/insights/modules/inflammation.py`
- `backend/core/insights/modules/fatigue_root_cause.py`
- `backend/core/insights/modules/detox_filtration.py`
- `backend/core/insights/modules/__init__.py` - Auto-import all modules

#### **Shared Calculations Module**
```python
# backend/core/data/derived_calculations.py
"""Shared derived metric calculations reused across insight modules."""

from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class DerivedMetrics:
    homa_ir: Optional[float] = None
    ldl_calculated: Optional[float] = None
    nlr: Optional[float] = None  # Neutrophil-to-lymphocyte ratio
    hdl_ldl_ratio: Optional[float] = None
    tg_hdl_ratio: Optional[float] = None

def calculate_derived_metrics(biomarkers: Dict[str, Any]) -> DerivedMetrics:
    """Calculate shared derived metrics from biomarker panel."""
    metrics = DerivedMetrics()
    
    # HOMA-IR calculation
    if all(k in biomarkers for k in ['glucose', 'insulin']):
        glucose = biomarkers['glucose']
        insulin = biomarkers['insulin']
        metrics.homa_ir = (glucose * insulin) / 405
    
    # LDL calculated (Friedewald equation)
    if all(k in biomarkers for k in ['total_cholesterol', 'hdl_cholesterol', 'triglycerides']):
        tc = biomarkers['total_cholesterol']
        hdl = biomarkers['hdl_cholesterol']
        tg = biomarkers['triglycerides']
        metrics.ldl_calculated = tc - hdl - (tg / 5)
    
    # Ratios
    if 'hdl_cholesterol' in biomarkers and 'ldl_cholesterol' in biomarkers:
        metrics.hdl_ldl_ratio = biomarkers['hdl_cholesterol'] / biomarkers['ldl_cholesterol']
    
    if 'triglycerides' in biomarkers and 'hdl_cholesterol' in biomarkers:
        metrics.tg_hdl_ratio = biomarkers['triglycerides'] / biomarkers['hdl_cholesterol']
    
    return metrics
```

#### **Module Template**
```python
from core.insights.base import BaseInsight, InsightMetadata, InsightResult
from core.insights.registry import register_insight
from core.models.context import AnalysisContext
from core.data.derived_calculations import calculate_derived_metrics

@register_insight("metabolic_age", "v1.0.0")
class MetabolicAgeInsight(BaseInsight):
    """
    Calculates biological age based on metabolic markers.
    
    Clinical Rationale:
    - Uses HOMA-IR, HbA1c, and age to estimate biological age
    - Thresholds: HOMA-IR > 2.5 indicates insulin resistance
    - Age adjustment: +5 years for each standard deviation above normal
    """
    
    @property
    def metadata(self) -> InsightMetadata:
        return InsightMetadata(
            insight_id="metabolic_age",
            version="v1.0.0",
            category="metabolic",
            required_biomarkers=["glucose", "hba1c", "insulin", "age"],
            optional_biomarkers=["bmi", "waist_circumference"],
            description="Calculates biological age based on metabolic markers",
            author="HealthIQ Team",
            created_at="2024-01-30T00:00:00Z",
            updated_at="2024-01-30T00:00:00Z"
        )
    
    def analyze(self, context: AnalysisContext) -> List[InsightResult]:
        """Analyze context and return structured results. Never raise exceptions."""
        try:
            # Extract biomarkers
            biomarkers = {k: v.value if hasattr(v, 'value') else v 
                         for k, v in context.biomarker_panel.biomarkers.items()}
            
            # Calculate derived metrics
            derived = calculate_derived_metrics(biomarkers)
            
            # Calculate metabolic age
            metabolic_age = self._calculate_metabolic_age(biomarkers, derived)
            
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",  # Will be set by orchestrator
                drivers={"homa_ir": derived.homa_ir, "hba1c": biomarkers.get('hba1c')},
                evidence={"metabolic_age": metabolic_age, "chronological_age": biomarkers.get('age')},
                biomarkers_involved=["glucose", "hba1c", "insulin", "age"],
                confidence=0.85,
                severity="info" if metabolic_age <= biomarkers.get('age', 0) + 5 else "warning"
            )]
            
        except Exception as e:
            return [InsightResult(
                insight_id=self.metadata.insight_id,
                version=self.metadata.version,
                manifest_id="",
                error_code="CALCULATION_FAILED",
                error_detail=str(e)
            )]

**Error Handling Rule**: All modules must catch exceptions and return a structured error result (`error_code`, `error_detail`), never raise.
    
    def _calculate_metabolic_age(self, biomarkers: Dict[str, Any], derived: DerivedMetrics) -> float:
        """Calculate metabolic age using HOMA-IR and HbA1c."""
        # Implementation here - simplified for example
        base_age = biomarkers.get('age', 35)
        if derived.homa_ir and derived.homa_ir > 2.5:
            return base_age + 5
        return base_age
```

#### **Tests to Implement**
- **Unit Tests**: Each module with fixture contexts
- **Golden Tests**: Deterministic modules with expected outputs
- **Integration Tests**: Module registration and discovery

---

### **Sprint 10a — Orchestrator Integration (2 weeks)**

#### **Definition of Ready**
- [ ] Sprint 9d modules complete
- [ ] All modules tested and stable
- [ ] Registry integration verified

#### **Definition of Done**
- [ ] Orchestrator uses manifest-driven dispatch
- [ ] Category-based synthesis removed
- [ ] Provenance persisted through existing persistence layer
- [ ] DTOs include provenance metadata
- [ ] Export service includes provenance
- [ ] End-to-end pipeline working
- [ ] Internal developer handover completed: update documentation, record short training/demo session on manifest-driven insights, and circulate updated developer guide

#### **Acceptance Criteria**
- [ ] Orchestrator loads active manifest
- [ ] Insights generated via registry lookup
- [ ] Provenance metadata persisted to database
- [ ] API responses include provenance fields
- [ ] Exports include provenance information
- [ ] Per-insight latency (`latency_ms`) and error counts are logged and exposed for monitoring
- [ ] After Sprint 10a, the `category` field will be formally deprecated and removed from DTOs and database schema in subsequent migration
- [ ] Prompts updated or confirmed compatible with modular outputs; test coverage in `test_insight_prompts.py` adjusted accordingly
- [ ] All integration tests passing

#### **Files to Modify**
- `backend/core/pipeline/orchestrator.py` - Replace category synthesis
- `backend/core/dto/builders.py` - Include provenance in DTOs
- `backend/services/storage/export_service.py` - Add provenance to exports
- `backend/core/insights/synthesis.py` - Update for modular insights
- `backend/core/insights/insight_prompts.py` - Audit and update for modular insights to ensure synthesis still functions as expected

#### **Orchestrator Changes**
```python
def synthesize_insights(self, context: AnalysisContext) -> Dict[str, Any]:
    # Load active manifest
    manifest = self.manifest_service.get_active_manifest()
    
    # Get enabled insights
    enabled_insights = manifest.get_enabled_insights()
    
    all_insights = []
    for config in enabled_insights:
        try:
            # Get insight module from registry
            insight_module = self.registry.get(config.insight_id, config.version)
            
            # Check if can analyze
            if insight_module.can_analyze(context):
                # Run analysis
                results = insight_module.analyze(context)
                
                # Add provenance metadata
                for result in results:
                    result.insight_id = config.insight_id
                    result.version = config.version
                    result.manifest_id = manifest.manifest_id
                    result.experiment_id = config.experiment_id
                
                all_insights.extend(results)
                
        except Exception as e:
            logger.error(f"Failed to run insight {config.insight_id}: {e}")
            continue
    
    return self._build_response(all_insights)
```

#### **Tests to Implement**
- **Integration Tests**: Full orchestrator pipeline
- **Contract Tests**: API response format validation
- **E2E Tests**: Complete analysis flow with provenance

---

### **Sprint 10b — Optional: Experiments and DB Manifests (2 weeks)**

#### **Definition of Ready**
- [ ] Sprint 10a orchestrator integration complete
- [ ] Basic modular system stable
- [ ] Business justification for experiments

#### **Definition of Done**
- [ ] Database manifest tables created
- [ ] Experiment service implemented
- [ ] Feature flags integrated
- [ ] A/B testing framework operational
- [ ] All tests passing

#### **Acceptance Criteria**
- [ ] Manifests can be stored in database
- [ ] Experiments can be configured
- [ ] Traffic splitting works deterministically
- [ ] Feature flags control insight execution
- [ ] Experiment results tracked

#### **Files to Create**
- `backend/core/models/insight_manifest.py` - Database manifest models
- `backend/services/insights/experiment_service.py` - A/B testing
- `backend/services/insights/feature_flags.py` - Feature flag service

---

### **Sprint 10c — Optional: Performance and Observability (2 weeks)**

#### **Definition of Ready**
- [ ] Sprint 10a complete
- [ ] Performance baseline established
- [ ] Monitoring requirements defined

#### **Definition of Done**
- [ ] Parallel insight execution implemented
- [ ] Performance metrics collected
- [ ] Benchmarks established
- [ ] Monitoring dashboard available

#### **Acceptance Criteria**
- [ ] Insights can run in parallel
- [ ] Performance metrics tracked
- [ ] No performance regression
- [ ] Monitoring alerts configured

---

## 🔧 **Interface Specifications**

### **BaseInsight Contract**
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
from core.models.context import AnalysisContext
from core.models.insight import Insight

@dataclass
class InsightMetadata:
    insight_id: str
    version: str
    category: str
    required_biomarkers: List[str]
    description: str
    author: str
    created_at: str
    updated_at: str

class BaseInsight(ABC):
    @property
    @abstractmethod
    def metadata(self) -> InsightMetadata:
        """Return insight metadata including ID, version, etc."""
        pass
    
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> List[Insight]:
        """Analyze context and generate insights."""
        pass
    
    def can_analyze(self, context: AnalysisContext) -> bool:
        """Check if insight can analyze the given context."""
        required = set(self.metadata.required_biomarkers)
        available = set(context.biomarker_panel.biomarkers.keys())
        return required.issubset(available)
```

### **Registry API**
```python
class InsightRegistry:
    def register(self, insight_id: str, version: str, insight_class: Type[BaseInsight]) -> None
    def get(self, insight_id: str, version: str) -> BaseInsight
    def get_all(self) -> List[BaseInsight]
    def list_versions(self, insight_id: str) -> List[str]
    def is_registered(self, insight_id: str, version: str) -> bool

def register_insight(insight_id: str, version: str):
    def decorator(cls):
        registry.register(insight_id, version, cls)
        return cls
    return decorator
```

### **ManifestService API**
```python
class ManifestService:
    def get_active_manifest(self) -> InsightManifest
    def get_enabled_insights(self) -> List[InsightConfig]
    def validate_manifest(self, manifest: Dict) -> bool
    def load_manifest(self, manifest_id: str) -> InsightManifest
    def save_manifest(self, manifest: InsightManifest) -> None
```

### **Orchestrator Call Sequence**
```python
# Pseudocode for manifest-driven synthesis
def synthesize_insights(self, context: AnalysisContext) -> Dict[str, Any]:
    # 1. Load active manifest
    manifest = self.manifest_service.get_active_manifest()
    
    # 2. Get enabled insights
    enabled_insights = manifest.get_enabled_insights()
    
    # 3. Process each insight
    all_insights = []
    for config in enabled_insights:
        if config.enabled:
            # 4. Get insight module
            insight_module = self.registry.get(config.insight_id, config.version)
            
            # 5. Check prerequisites
            if insight_module.can_analyze(context):
                # 6. Run analysis
                results = insight_module.analyze(context)
                
                # 7. Add provenance
                for result in results:
                    result.insight_id = config.insight_id
                    result.version = config.version
                    result.manifest_id = manifest.manifest_id
                
                all_insights.extend(results)
    
    # 8. Build response
    return self._build_response(all_insights)
```

---

## 🧪 **Testing Strategy**

### **Test Pyramid Structure**

#### **Unit Tests (70%)**
- **Registry Tests**: Registration, retrieval, duplicate prevention
- **Manifest Tests**: Validation, loading, error handling
- **Module Tests**: Each insight module with fixtures
- **DTO Tests**: Provenance field inclusion
- **Contract Tests**: BaseInsight interface compliance

#### **Integration Tests (25%)**
- **Orchestrator Tests**: Full synthesis pipeline
- **Persistence Tests**: Provenance storage and retrieval
- **Export Tests**: Provenance in exports
- **Manifest Service Tests**: Database integration

#### **E2E Tests (5%)**
- **Full Pipeline Tests**: Upload → Analysis → Export with provenance
- **API Contract Tests**: Response format validation
- **Performance Tests**: No regression in analysis time

### **Test Fixtures**
```python
# Sample context fixture
@pytest.fixture
def analysis_context():
    return AnalysisContext(
        analysis_id="test_analysis_123",
        user=User(age=35, gender="male"),
        biomarker_panel=BiomarkerPanel({
            "glucose": BiomarkerValue(95, "mg/dL"),
            "hba1c": BiomarkerValue(5.2, "%"),
            "insulin": BiomarkerValue(8.5, "μU/mL")
        })
    )

# Sample manifest fixture
@pytest.fixture
def test_manifest():
    return {
        "manifest_id": "test_v1",
        "version": "1",
        "insights": [
            {"insight_id": "metabolic_age", "version": "v1", "enabled": True}
        ]
    }
```

### **Determinism Guidelines**
- **Mock LLM Responses**: Use deterministic mock responses for consistent testing
- **Fixed Timestamps**: Use fixed timestamps in test data
- **Seeded Random**: Use seeded random for any probabilistic operations
- **Golden Outputs**: Store expected outputs for deterministic modules

### **Mocking Rules**
- **External Dependencies**: Mock database, LLM, file system
- **Time-Dependent**: Mock timestamps and time-based operations
- **Random Operations**: Mock random number generation
- **Network Calls**: Mock any external API calls

### **Minimum Green Gates**
- **100% Pass Rate**: All new unit tests must pass
- **Integration Coverage**: All integration tests must pass
- **E2E Smoke**: At least one full pipeline test must pass
- **Performance Baseline**: No regression in analysis time

### **CI Job Commands**
```bash
# Unit tests
cd backend && python -m pytest tests/unit/test_insights/ -v

# Integration tests  
cd backend && python -m pytest tests/integration/test_insight_pipeline/ -v

# E2E tests
cd backend && python -m pytest tests/e2e/test_insight_modularity/ -v

# Performance tests
cd backend && python -m pytest tests/performance/test_insight_performance/ -v
```

---

## ⚠️ **Risk Register and Mitigations**

### **High Risk**

#### **Test Churn (Impact: High, Probability: High)**
- **Risk**: 20+ tests reference hardcoded categories
- **Mitigation**: 
  - Comprehensive test audit before starting
  - Test migration plan with backward compatibility
  - Automated test discovery and update tools
- **Rollback**: Revert to category-based tests if needed

#### **Frontend Compatibility (Impact: High, Probability: Medium)**
- **Risk**: DTO changes break frontend expectations
- **Mitigation**:
  - Maintain backward-compatible DTO structure
  - Add provenance fields as optional initially
  - Frontend compatibility testing
- **Rollback**: Revert DTO changes, maintain old structure

#### **Database Migration Failure (Impact: High, Probability: Low)**
- **Risk**: Schema changes cause data loss or corruption
- **Mitigation**:
  - Incremental migration with rollback plan
  - Data backup before migration
  - Migration testing on copy of production data
- **Rollback**: Database rollback to previous schema

### **Medium Risk**

#### **Performance Regression (Impact: Medium, Probability: Medium)**
- **Risk**: Sequential insight execution slower than category-based
- **Mitigation**:
  - Performance benchmarking before/after
  - Parallel execution ready for future implementation
  - Performance monitoring and alerts
- **Rollback**: Revert to category-based synthesis

#### **LLM Integration Changes (Impact: Medium, Probability: Low)**
- **Risk**: LLM prompts need updates for modular insights
- **Mitigation**:
  - Keep existing prompt templates where possible
  - Gradual prompt migration
  - A/B test new prompts
- **Rollback**: Revert to original prompt templates

### **Low Risk**

#### **Configuration Drift (Impact: Low, Probability: Medium)**
- **Risk**: Manifests become inconsistent or invalid
- **Mitigation**:
  - JSON schema validation
  - Automated manifest testing
  - Configuration version control
- **Rollback**: Revert to previous manifest version

#### **Learning Curve (Impact: Low, Probability: High)**
- **Risk**: Team needs time to understand new system
- **Mitigation**:
  - Comprehensive documentation
  - Training sessions
  - Code examples and tutorials
- **Rollback**: N/A (training issue)

#### **Result Explosion (Impact: Medium, Probability: Medium)**
- **Risk**: Modules that emit multiple sub-insights could bloat payload
- **Mitigation**: 
  - Cap per-module outputs (max 3 insights per module)
  - Require `result_key` scoping for sub-insights
  - Monitor payload size in tests
- **Rollback**: Implement result capping if needed

#### **Manifest Drift (Impact: Medium, Probability: Low)**
- **Risk**: Manifests become inconsistent with registry
- **Mitigation**:
  - Add CI job `validate:manifest` that imports registry and fails if any `(id,version)` missing
  - Pre-commit hooks for manifest validation
  - Automated manifest testing
- **Rollback**: Revert to previous manifest version

#### **Category Test Residue (Impact: Low, Probability: High)**
- **Risk**: Category assertions cause false test failures
- **Mitigation**:
  - Delete or rewrite category assertions early in Sprint 9c
  - Comprehensive test audit before starting
  - Automated test discovery and update tools
- **Rollback**: Temporarily disable failing tests during transition

---

## 📝 **Change Log and Developer Checklist**

### **PR Checklist**

#### **Before Implementation**
- [ ] Current architecture audited
- [ ] Test migration plan created
- [ ] Database migration strategy confirmed
- [ ] Frontend compatibility verified

#### **During Implementation**
- [ ] All new unit tests written and passing
- [ ] Integration tests updated
- [ ] Database migration tested
- [ ] DTO changes validated
- [ ] Export service updated

#### **Before Merge**
- [ ] All tests passing (100% pass rate)
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Manual validation completed

### **Manual Validation Steps**

#### **Sprint 9c Validation**
```bash
# 1. Test registry functionality
cd backend && python -c "
from core.insights.registry import insight_registry
from core.insights.modules import *  # Auto-import modules
print('Registered insights:', insight_registry.get_all())
"

# 2. Test manifest loading
cd backend && python -c "
from services.insights.manifest_service import ManifestService
service = ManifestService()
manifest = service.get_active_manifest()
print('Active manifest:', manifest.manifest_id)
"

# 3. Test database migration
cd backend && alembic upgrade head
cd backend && python -c "
from core.models.database import Insight
from config.database import get_db
db = next(get_db())
insights = db.query(Insight).limit(1).all()
print('Insight with provenance:', insights[0].insight_id if insights else 'No insights')
"
```

#### **Sprint 9d Validation**
```bash
# 1. Test module registration
cd backend && python -c "
from core.insights.modules import *
from core.insights.registry import insight_registry
print('Available modules:', [insight.metadata.insight_id for insight in insight_registry.get_all()])
"

# 2. Test module analysis
cd backend && python -c "
from core.insights.modules.metabolic_age import MetabolicAgeInsight
from tests.fixtures import analysis_context
insight = MetabolicAgeInsight()
context = analysis_context()
print('Can analyze:', insight.can_analyze(context))
"
```

#### **Sprint 10a Validation**
```bash
# 1. Test full orchestrator pipeline
cd backend && python -c "
from core.pipeline.orchestrator import AnalysisOrchestrator
from tests.fixtures import analysis_context
orchestrator = AnalysisOrchestrator()
context = analysis_context()
result = orchestrator.synthesize_insights(context)
print('Generated insights:', len(result['insights']))
print('First insight provenance:', result['insights'][0].get('insight_id') if result['insights'] else 'No insights')
"

# 2. Test API endpoint
curl -X POST http://localhost:8000/api/analysis/start \
  -H "Content-Type: application/json" \
  -d '{"biomarkers": {"glucose": 95}, "user": {"age": 35, "sex": "male"}}'
```

### **Developer Workflow**

#### **Pre-commit Hooks**
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-manifest
        name: Validate insight manifest
        entry: python scripts/validate_manifest.py
        language: python
        files: ^backend/data/insight_manifests/.*\.json$
        # Manifest validation must also run in CI; the build fails if any (insight_id, version) in manifest is missing from registry
      - id: ruff
        name: Run ruff
        entry: ruff check --fix
        language: python
        files: ^backend/.*\.py$
      - id: mypy
        name: Run mypy
        entry: mypy
        language: python
        files: ^backend/.*\.py$
```

#### **Make Targets**
```makefile
# Makefile
.PHONY: insights-validate insights-test insights-migrate

insights-validate:
	@echo "Validating insight registry and manifest..."
	python scripts/validate_insights.py
	python scripts/validate_manifest.py

insights-test:
	@echo "Running insight unit and golden tests..."
	python -m pytest tests/unit/test_insights/ -v
	python -m pytest tests/unit/test_insight_modules/ -v

insights-migrate:
	@echo "Running database migration and smoke test..."
	cd backend && alembic upgrade head
	python scripts/smoke_test_insights.py
```

#### **Validation Scripts**
```python
# scripts/validate_insights.py
"""Validate insight registry and manifest consistency."""

from core.insights.registry import insight_registry
from services.insights.manifest_service import ManifestService

def validate_insights():
    """Ensure all insights are properly registered."""
    registry.ensure_insights_registered()
    registered = registry.get_all()
    print(f"✅ {len(registered)} insights registered")
    
    for insight in registered:
        print(f"  - {insight.metadata.insight_id} v{insight.metadata.version}")

def validate_manifest():
    """Validate manifest against registry."""
    service = ManifestService()
    manifest = service.get_active_manifest()
    
    for config in manifest.insights:
        try:
            registry.assert_registered(config.insight_id, config.version)
            print(f"✅ {config.insight_id} v{config.version} registered")
        except KeyError:
            print(f"❌ {config.insight_id} v{config.version} NOT registered")
            raise

if __name__ == "__main__":
    validate_insights()
    validate_manifest()
```

### **Post-Merge Monitoring**

#### **Key Metrics to Track**
- **Analysis Success Rate**: Should remain at 100%
- **Insight Generation Time**: Should not increase significantly
- **Database Query Performance**: Monitor insight table queries
- **Error Rates**: Track insight generation failures
- **Test Coverage**: Maintain 100% pass rate
- **Manifest Validation**: Monitor manifest consistency

#### **Alerts to Configure**
- **Test Failures**: Alert on any test failures
- **Performance Regression**: Alert if analysis time increases >20%
- **Database Errors**: Alert on insight table query failures
- **Manifest Errors**: Alert on manifest validation failures
- **Registry Errors**: Alert on missing insight registrations

---

## 🔍 **As-Is Verification**

### **Current Architecture Audit**

#### **Category Synthesis Locations**
- **Primary**: `backend/core/pipeline/orchestrator.py:430-562` - `synthesize_insights()` method
- **Secondary**: `backend/core/insights/synthesis.py:282-584` - `InsightSynthesizer.synthesize_insights()`
- **Tests**: 20+ test files reference hardcoded categories

#### **Current Insights Schema**
```sql
-- Current insights table structure
CREATE TABLE insights (
    id UUID PRIMARY KEY,
    analysis_id UUID NOT NULL,
    insight_type VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- Hardcoded categories
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    -- ... other fields
);

-- Indexes that will need updating
CREATE INDEX idx_insights_category ON insights(category);
CREATE INDEX idx_insights_analysis_category ON insights(analysis_id, category);
```

#### **DTO Shapes**
```typescript
// Frontend expects this structure
interface InsightData {
  insight_id: string;      // ✅ Already exists
  title: string;
  description: string;
  category: string;        // ✅ Will be preserved
  confidence: number;
  severity: string;
  biomarkers: string[];
  recommendations: string[];
  // Missing: version, manifest_id, experiment_id
}
```

#### **Tests That Will Break**
- `backend/tests/unit/test_insight_synthesis.py` - 15+ tests reference categories
- `backend/tests/integration/test_insight_pipeline_integration.py` - 10+ tests
- `backend/tests/unit/test_insight_prompts.py` - 5+ tests
- All tests that assert `insight.category in ["metabolic", "cardiovascular", "inflammatory"]`

### **Red Flags Identified**

#### **1. Test Churn (HIGH IMPACT)**
- **Issue**: 20+ tests hardcode category expectations
- **Solution**: Comprehensive test migration plan
- **Timeline**: Add 2-3 days to Sprint 9c for test updates

#### **2. Database Index Dependencies (MEDIUM IMPACT)**
- **Issue**: Category-based indexes will become less useful
- **Solution**: Add new indexes, keep old ones for compatibility
- **Timeline**: Add to migration script

#### **3. Frontend DTO Compatibility (LOW IMPACT)**
- **Issue**: Frontend expects specific insight structure
- **Solution**: Maintain backward-compatible DTO structure
- **Timeline**: No additional time needed

#### **4. LLM Prompt Coupling (LOW IMPACT)**
- **Issue**: Prompts are category-specific
- **Solution**: Keep existing prompts, add insight-specific prompts later
- **Timeline**: No additional time needed

### **Scope Adjustments Based on Audit**

#### **Sprint 9c Adjustments**
- **Add Test Migration**: 2-3 days for comprehensive test updates
- **Add Index Strategy**: Plan for both old and new indexes
- **Add DTO Compatibility**: Ensure frontend compatibility

#### **Sprint 9d Adjustments**
- **Add Golden Tests**: For deterministic insight modules
- **Add Module Discovery**: Auto-import system for modules

#### **Sprint 10a Adjustments**
- **Add Performance Testing**: Ensure no regression
- **Add Contract Testing**: Validate API response format

---

## 📊 **Success Metrics**

### **Sprint 9c Success**
- [ ] Registry prevents duplicate registrations
- [ ] Manifest validates against JSON schema
- [ ] Database migration runs without data loss
- [ ] DTOs include provenance fields
- [ ] 100% pass rate on new unit tests
- [ ] `ensure_insights_registered()` returns ≥5 registered classes
- [ ] Manifest validation fails if any `(id,version)` absent

### **Sprint 9d Success**
- [ ] All 5 modules load via registry
- [ ] Each module implements required metadata
- [ ] Modules generate valid InsightResult objects
- [ ] 100% pass rate on module tests
- [ ] Golden parity with v4 for the five insights within ±1% tolerance
- [ ] Shared calculations module prevents duplication

### **Sprint 10a Success**
- [ ] Orchestrator uses manifest-driven dispatch
- [ ] Provenance persisted to database
- [ ] API responses include provenance and stable ordering
- [ ] Exports include provenance
- [ ] 100% pass rate on integration tests
- [ ] DB enforces uniqueness constraint
- [ ] Category synthesis fully removed

### **Overall Success**
- [ ] Zero production incidents
- [ ] No performance regression
- [ ] Full test coverage maintained
- [ ] Documentation complete
- [ ] Team trained on new system

---

## 🔄 **Rollback Plan**

### **If Orchestrator Refactor Fails (Sprint 10a)**
- **Immediate Action**: Since there are no production users, rollback can primarily be achieved by disabling failing insights in manifest. The category-mode fallback should be considered a last-resort safety net only.
- **Code Changes**: 
  ```python
  # In orchestrator.py
  if os.getenv("INSIGHTS_ENGINE") == "category":
      return self._legacy_category_synthesis(context)
  else:
      return self._manifest_driven_synthesis(context)
  ```
- **Timeline**: One branch only, remove after 10a completion
- **Data Impact**: No data loss, legacy insights continue working
- **Rollback Steps**:
  1. Disable problematic insights in manifest (`enabled: false`)
  2. Monitor for stability
  3. Fix modular system issues
  4. Re-enable insights in manifest
  5. If critical, set `INSIGHTS_ENGINE=category` as last resort

### **If Database Migration Fails**
- **Immediate Action**: Rollback database migration
- **Command**: `cd backend && alembic downgrade -1`
- **Data Impact**: Minimal - new columns will be lost, existing data preserved
- **Recovery**: Re-run migration after fixing issues

### **If Module Registration Fails**
- **Immediate Action**: Disable problematic modules in manifest
- **Code Changes**: Set `enabled: false` for failing modules
- **Impact**: Reduced insight coverage, but system remains stable
- **Recovery**: Fix modules and re-enable

### **If Performance Degrades**
- **Immediate Action**: Revert to category synthesis
- **Monitoring**: Set performance alerts at 20% degradation threshold
- **Investigation**: Profile modular system for bottlenecks
- **Recovery**: Optimize or implement parallel execution

### **Rollback Validation**
- [ ] All tests pass with rollback configuration
- [ ] API responses match previous format
- [ ] Database queries perform within baseline
- [ ] No data corruption or loss
- [ ] Frontend compatibility maintained

---

This comprehensive refactor plan provides a clear path to transform the current category-based insight system into a modular, versioned, manifest-driven insights engine with full provenance tracking. The plan addresses all identified risks and provides detailed implementation guidance for each sprint.
