# HealthIQ Clean Architecture Skeleton
## Data Flow: Upload → Clustering → Visualization

```
📤 User Upload → 🔄 Normalization → 🧠 Analysis → 📊 Visualization
```

## 📁 Project Structure

```
healthiq/
├── backend/
│   ├── api/                           # FastAPI routes & validation
│   │   ├── __init__.py
│   │   ├── upload.py                  # POST /upload/biomarkers
│   │   ├── analysis.py                # GET /analysis/{panel_id}
│   │   └── insights.py                # GET /insights/{panel_id}
│   │
│   ├── core/                          # Business logic core
│   │   ├── models/                    # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── biomarker.py           # BiomarkerValue, BiomarkerPanel
│   │   │   ├── user.py                # UserProfile, Demographics
│   │   │   ├── analysis.py            # AnalysisContext, AnalysisResult
│   │   │   └── insights.py            # InsightResult, ClusterResult
│   │   │
│   │   ├── pipeline/                  # Core processing pipeline
│   │   │   ├── __init__.py
│   │   │   ├── normalizer.py          # Raw data → canonical biomarkers
│   │   │   ├── enricher.py            # Add ranges, flags, metadata
│   │   │   ├── clusterer.py           # Biomarker clustering engine (USP)
│   │   │   └── orchestrator.py        # Main pipeline coordinator
│   │   │
│   │   ├── insights/                  # Health insight engines
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # BaseInsight abstract class
│   │   │   ├── cardiovascular.py      # Heart health analysis
│   │   │   ├── metabolic.py           # Glucose/insulin analysis
│   │   │   ├── inflammation.py        # Inflammatory markers
│   │   │   └── registry.py            # Insight discovery & execution
│   │   │
│   │   ├── clustering/                # Biomarker clustering (USP)
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # Core clustering algorithms
│   │   │   ├── rules.py               # Clustering rule definitions
│   │   │   ├── validators.py          # Cluster validation logic
│   │   │   └── scorers.py             # Cluster scoring functions
│   │   │
│   │   └── services/                  # Application services
│   │       ├── __init__.py
│   │       ├── analysis_service.py    # Analysis orchestration
│   │       ├── storage_service.py     # Data persistence
│   │       └── notification_service.py # Results delivery
│   │
│   ├── utils/                         # Shared utilities
│   │   ├── __init__.py
│   │   ├── biomarker_aliases.py       # Name normalization
│   │   ├── ranges.py                  # Reference ranges
│   │   └── validators.py              # Common validation
│   │
│   └── tests/                         # Comprehensive testing
│       ├── unit/                      # Unit tests by module
│       ├── integration/               # Pipeline integration tests
│       └── fixtures/                  # Test data
│
├── frontend/                          # React/Next.js frontend
│   ├── components/
│   │   ├── upload/                    # File upload interface
│   │   ├── analysis/                  # Analysis results display
│   │   ├── insights/                  # Insight visualization
│   │   └── clusters/                  # Cluster visualization (USP)
│   │
│   ├── pages/
│   │   ├── upload.tsx                 # Upload biomarker data
│   │   ├── dashboard.tsx              # Analysis overview
│   │   └── insights/[id].tsx          # Detailed insight view
│   │
│   └── lib/
│       ├── api.ts                     # Backend API client
│       └── types.ts                   # TypeScript definitions
│
└── shared/                            # Shared types & schemas
    ├── schemas/                       # OpenAPI/JSON schemas
    └── types/                         # TypeScript definitions
```

## 🔄 Data Flow Architecture

### **1. Data Ingestion Layer**

```python
# api/upload.py - User data entry point
@router.post("/upload/biomarkers")
async def upload_biomarkers(
    file: UploadFile,
    user_id: str = Header(),
) -> UploadResponse:
    """Upload biomarker data (CSV, PDF, JSON)"""
    
    # Parse uploaded file
    raw_data = await parse_upload(file)
    
    # Create analysis request
    analysis_id = await analysis_service.create_analysis(
        user_id=user_id,
        raw_biomarkers=raw_data
    )
    
    return UploadResponse(analysis_id=analysis_id, status="processing")
```

### **2. Data Normalization Layer**

```python
# core/pipeline/normalizer.py - Clean & standardize data
class BiomarkerNormalizer:
    """Convert raw uploads to canonical biomarker format"""
    
    def normalize(self, raw_data: Dict) -> BiomarkerPanel:
        """
        Raw data → Canonical biomarkers
        
        Examples:
        "Fasting Glucose" → "fasting_glucose"
        "HbA1c %" → "hba1c"
        "Total Cholesterol" → "total_cholesterol"
        """
        
        canonical_biomarkers = {}
        
        for raw_name, value in raw_data.items():
            # Resolve to canonical name
            canonical_name = self.alias_resolver.resolve(raw_name)
            
            # Create validated biomarker
            biomarker = BiomarkerValue(
                value=value,
                canonical_name=canonical_name,
                original_name=raw_name,
                unit=self.detect_unit(value, canonical_name)
            )
            
            canonical_biomarkers[canonical_name] = biomarker
        
        return BiomarkerPanel(
            biomarkers=canonical_biomarkers,
            metadata=self.extract_metadata(raw_data)
        )
```

### **3. Biomarker Clustering Engine (USP)**

```python
# core/clustering/engine.py - Your competitive advantage
class BiomarkerClusterEngine:
    """Advanced biomarker pattern recognition and clustering"""
    
    def analyze_clusters(self, panel: BiomarkerPanel) -> List[ClusterResult]:
        """
        Identify biomarker patterns and health clusters
        
        Example clusters:
        - Metabolic Syndrome: glucose + insulin + triglycerides
        - Inflammation: CRP + ESR + fibrinogen  
        - Cardiovascular Risk: cholesterol ratios + homocysteine
        """
        
        clusters = []
        
        # Apply clustering rules
        for rule in self.clustering_rules:
            if rule.can_apply(panel):
                cluster = rule.evaluate(panel)
                if cluster.is_significant():
                    clusters.append(cluster)
        
        # Score and rank clusters
        return self.score_clusters(clusters)

class ClusteringRule:
    """Individual clustering logic"""
    
    def __init__(self, name: str, required_biomarkers: List[str]):
        self.name = name
        self.required_biomarkers = required_biomarkers
    
    def can_apply(self, panel: BiomarkerPanel) -> bool:
        """Check if panel has required biomarkers"""
        return panel.has_biomarkers(self.required_biomarkers)
    
    def evaluate(self, panel: BiomarkerPanel) -> ClusterResult:
        """Apply clustering algorithm"""
        # Implement specific clustering logic
        pass

# Example clustering rules
METABOLIC_SYNDROME_RULE = ClusteringRule(
    name="metabolic_syndrome",
    required_biomarkers=["fasting_glucose", "triglycerides", "hdl_cholesterol"]
)

INFLAMMATION_CLUSTER_RULE = ClusteringRule(
    name="systemic_inflammation", 
    required_biomarkers=["crp", "esr"]
)
```

### **4. Health Insights Layer**

```python
# core/insights/base.py - Standardized insight interface
class BaseInsight(ABC):
    """Abstract base for all health insights"""
    
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> Optional[InsightResult]:
        """Generate health insight from analysis context"""
        pass
    
    @abstractmethod
    def required_biomarkers(self) -> List[str]:
        """Biomarkers needed for this insight"""
        pass

# core/insights/cardiovascular.py - Example insight
class CardiovascularInsight(BaseInsight):
    """Heart health analysis using biomarker clusters"""
    
    def required_biomarkers(self) -> List[str]:
        return ["total_cholesterol", "hdl_cholesterol", "triglycerides"]
    
    def analyze(self, context: AnalysisContext) -> Optional[InsightResult]:
        """Analyze cardiovascular risk from biomarker patterns"""
        
        # Use cluster results for enhanced analysis
        cardio_clusters = context.get_clusters_by_type("cardiovascular")
        
        # Calculate risk score
        risk_score = self.calculate_risk(context.biomarkers, cardio_clusters)
        
        return InsightResult(
            insight_id="cardiovascular_risk",
            title="Cardiovascular Health Assessment",
            score=risk_score,
            cluster_contributions=cardio_clusters,
            recommendations=self.generate_recommendations(risk_score)
        )
```

### **5. Analysis Orchestration**

```python
# core/pipeline/orchestrator.py - Main processing pipeline
class AnalysisOrchestrator:
    """Coordinate the complete analysis pipeline"""
    
    def __init__(self):
        self.normalizer = BiomarkerNormalizer()
        self.clusterer = BiomarkerClusterEngine()
        self.insight_registry = InsightRegistry()
    
    async def process_analysis(self, analysis_id: str) -> AnalysisResult:
        """Execute complete biomarker analysis pipeline"""
        
        # 1. Load raw data
        raw_data = await self.storage.get_raw_data(analysis_id)
        
        # 2. Normalize biomarkers
        panel = self.normalizer.normalize(raw_data)
        
        # 3. Perform clustering analysis (USP)
        clusters = self.clusterer.analyze_clusters(panel)
        
        # 4. Create analysis context
        context = AnalysisContext(
            panel=panel,
            clusters=clusters,
            user_profile=await self.get_user_profile(analysis_id)
        )
        
        # 5. Generate insights
        insights = []
        for insight_class in self.insight_registry.get_applicable_insights(context):
            insight = insight_class()
            result = insight.analyze(context)
            if result:
                insights.append(result)
        
        # 6. Create final result
        return AnalysisResult(
            analysis_id=analysis_id,
            biomarker_panel=panel,
            clusters=clusters,  # USP: Rich cluster analysis
            insights=insights,
            generated_at=datetime.utcnow()
        )
```

### **6. API Response Layer**

```python
# api/analysis.py - Results delivery
@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> AnalysisResponse:
    """Get complete analysis results including clusters"""
    
    result = await analysis_service.get_analysis(analysis_id)
    
    return AnalysisResponse(
        biomarkers=result.panel.to_dict(),
        clusters=[
            {
                "cluster_id": c.cluster_id,
                "name": c.name,
                "biomarkers": c.contributing_biomarkers,
                "significance_score": c.score,
                "health_impact": c.health_implications
            }
            for c in result.clusters
        ],
        insights=[
            {
                "insight_id": i.insight_id,
                "title": i.title,
                "score": i.score,
                "related_clusters": i.cluster_contributions,
                "recommendations": i.recommendations
            }
            for i in result.insights
        ]
    )
```

### **7. Frontend Visualization**

```typescript
// components/clusters/ClusterVisualization.tsx
interface ClusterVisualizationProps {
  clusters: ClusterResult[];
  biomarkers: BiomarkerPanel;
}

export const ClusterVisualization: React.FC<ClusterVisualizationProps> = ({
  clusters,
  biomarkers
}) => {
  return (
    <div className="cluster-analysis">
      <h2>Biomarker Cluster Analysis</h2>
      
      {clusters.map(cluster => (
        <ClusterCard key={cluster.cluster_id}>
          <ClusterHeader>
            <h3>{cluster.name}</h3>
            <ScoreBadge score={cluster.significance_score} />
          </ClusterHeader>
          
          <BiomarkerNetwork 
            biomarkers={cluster.contributing_biomarkers}
            connections={cluster.biomarker_relationships}
          />
          
          <HealthImpact impact={cluster.health_implications} />
          
          <RelatedInsights insights={cluster.related_insights} />
        </ClusterCard>
      ))}
    </div>
  );
};
```

## 🎯 Core Data Models

```python
# core/models/biomarker.py
class BiomarkerValue(BaseModel):
    """Individual biomarker measurement"""
    value: float
    unit: Optional[str]
    canonical_name: str
    original_name: str
    reference_range: Optional[Tuple[float, float]]
    flags: List[str] = []

class BiomarkerPanel(BaseModel):
    """Complete set of biomarker measurements"""
    panel_id: str
    biomarkers: Dict[str, BiomarkerValue]
    timestamp: datetime
    metadata: Dict[str, Any] = {}

# core/models/analysis.py  
class ClusterResult(BaseModel):
    """Biomarker cluster analysis result (USP)"""
    cluster_id: str
    name: str
    contributing_biomarkers: List[str]
    significance_score: float
    health_implications: str
    biomarker_relationships: Dict[str, Any]

class AnalysisContext(BaseModel):
    """Complete analysis context"""
    panel: BiomarkerPanel
    clusters: List[ClusterResult]
    user_profile: UserProfile
    
    class Config:
        frozen = True  # Immutable

class InsightResult(BaseModel):
    """Health insight result"""
    insight_id: str
    title: str
    score: float
    cluster_contributions: List[str]  # Which clusters influenced this insight
    recommendations: List[str]
    confidence: float
```

## 🚀 Implementation Priority

**Phase 1 (Week 1)**: Core models + normalization + basic clustering  
**Phase 2 (Week 2)**: Orchestrator + 3 core insights + API  
**Phase 3 (Week 3)**: Advanced clustering rules + frontend visualization  
**Phase 4 (Week 4)**: Full insight suite + testing + deployment  

This architecture puts **biomarker clustering at the center** as your competitive advantage, with clean data flow and type safety throughout.