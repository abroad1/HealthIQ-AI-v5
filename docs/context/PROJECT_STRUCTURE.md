# Project Structure

> 🛠️ Architectural Blueprint Notice:  
> This document defines the **planned, canonical folder structure** for the full HealthIQ AI v5 application.  
> It is a **forward-looking design**, not a reflection of the current file tree.  
> Cursor agents and developers must treat this as a blueprint for how the application **should be structured over time**.  
> Do not modify or delete paths based on present-day repo mismatches — many directories listed here are intentionally unbuilt or deferred.

> For our AI/LLM strategy, see [`LLM_POLICY.md`](./LLM_POLICY.md)

This document defines the intended repository layout for HealthIQ-AI v5. This structure serves as the source of truth for all future scaffolding and agent-generated file placement.

### Current vs Planned Structure

This document defines the **target file structure** for HealthIQ AI v5.  
Some folders and files may not exist yet.  
Cursor agents should use this as a blueprint for system organisation and future expansion—not a mirror of the current file tree.

```
healthiq/
├── backend/                           # FastAPI-based AI analysis backend
│   ├── app/                          # FastAPI application layer
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point with CORS config
│   │   └── routes/                   # API route handlers
│   │       ├── __init__.py
│   │       ├── health.py             # Health check endpoints
│   │       ├── analysis.py           # Biomarker analysis endpoints
│   │       ├── auth.py               # Authentication & authorization
│   │       ├── users.py              # User management endpoints
│   │       └── reports.py            # Report generation endpoints
│   ├── core/                         # Core business logic and domain models
│   │   ├── __init__.py
│   │   ├── models/                   # Domain models and data structures
│   │   │   ├── __init__.py
│   │   │   ├── biomarker.py          # Biomarker data models
│   │   │   ├── user.py               # User profile and preferences
│   │   │   ├── context.py            # Analysis context and metadata
│   │   │   ├── results.py            # Analysis results and insights
│   │   │   └── reports.py            # Report data models
│   │   ├── pipeline/                 # Analysis pipeline orchestration
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py       # orchestrates: score → clusters → insights → dto
│   │   │   ├── context_factory.py    # Creates analysis context from user data
│   │   │   ├── events.py             # Pipeline event handling
│   │   │   └── middleware.py         # Pipeline processing middleware
│   │   ├── canonical/                # Data normalization and standardization
│   │   │   ├── __init__.py
│   │   │   ├── normalize.py          # Biomarker value normalization
│   │   │   └── resolver.py           # Unit conversion and reference ranges
│   │   ├── clustering/               # AI clustering algorithms
│   │   │   ├── __init__.py
│   │   │   ├── engine.py             # Clustering algorithm implementations
│   │   │   └── rules.py              # Clustering rules and thresholds
│   │   ├── scoring/                  # Biomarker scoring engine (placeholder)
│   │   │   ├── __init__.py
│   │   │   ├── engine.py             # Scoring algorithm implementations
│   │   │   └── rules.py              # Scoring rules and thresholds
│   │   ├── insights/                 # AI insight generation
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Base insight classes
│   │   │   ├── registry.py           # Insight type registry
│   │   │   ├── generators/           # Specific insight generators
│   │   │   │   ├── __init__.py
│   │   │   │   ├── biomarker.py      # Biomarker-specific insights
│   │   │   │   ├── trend.py          # Trend analysis insights
│   │   │   │   └── risk.py           # Risk assessment insights
│   │   │   └── validators/           # Insight validation logic
│   │   │       ├── __init__.py
│   │   │       └── medical.py        # Medical accuracy validation
│   │   └── dto/                      # Data Transfer Objects
│   │       ├── __init__.py
│   │       └── builders.py           # DTO construction and mapping
│   ├── services/                     # External service integrations
│   │   ├── __init__.py
│   │   ├── ai/                       # Gemini LLM service integrations
│   │   │   ├── __init__.py
│   │   │   ├── gemini.py             # Google Gemini API integration
│   │   │   └── local_models.py       # Local ML model inference
│   │   ├── storage/                  # Data storage services
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # Database operations
│   │   │   └── cache.py              # Redis/caching layer
│   │   └── external/                 # Third-party API integrations
│   │       ├── __init__.py
│   │       └── medical_apis.py       # Medical data APIs
│   ├── utils/                        # Utility functions and helpers
│   │   ├── __init__.py
│   │   ├── validators.py             # Data validation utilities
│   │   ├── formatters.py             # Data formatting utilities
│   │   └── security.py               # Security and encryption utilities
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   ├── env.py                    # Secure environment variable access
│   │   ├── settings.py               # Application settings
│   │   ├── database.py               # Database configuration
│   │   └── ai.py                     # Gemini LLM configuration
│   ├── tests/                        # Backend test suite
│   │   ├── __init__.py
│   │   ├── unit/                     # Unit tests
│   │   ├── integration/              # Integration tests
│   │   ├── e2e/                      # End-to-end tests
│   │   └── fixtures/                 # Test data and fixtures
│   ├── ssot/                         # Single Source of Truth data
│   │   ├── biomarkers.yaml           # Biomarker definitions and ranges
│   │   ├── ranges.yaml               # Reference ranges by population
│   │   ├── units.yaml                # Unit conversion definitions
│   │   └── medical_terms.yaml        # Medical terminology dictionary
│   ├── tools/                        # Development and deployment tools
│   │   ├── __init__.py
│   │   ├── export_openapi.py         # OpenAPI schema export
│   │   ├── data_migration.py         # Database migration tools
│   │   └── model_training.py         # Gemini model training scripts
│   ├── docs/                         # Backend-specific documentation
│   │   └── openapi.yaml              # OpenAPI specification
│   ├── requirements.txt              # Python dependencies
│   ├── pyproject.toml                # Python project configuration
│   ├── mypy.ini                      # Type checking configuration
│   └── README.md                     # Backend documentation
├── frontend/                         # Next.js 14+ App Router frontend (PLANNED)
│   ├── app/                          # Next.js App Router (file-system routing)
│   │   ├── layout.tsx                # Root layout component
│   │   ├── page.tsx                  # Homepage
│   │   ├── loading.tsx               # Global loading UI
│   │   ├── error.tsx                 # Global error UI
│   │   ├── not-found.tsx             # 404 page
│   │   ├── dashboard/                # Dashboard pages
│   │   │   ├── page.tsx              # Main dashboard
│   │   │   └── loading.tsx           # Dashboard loading UI
│   │   ├── analysis/                 # Analysis pages
│   │   │   ├── page.tsx              # Analysis input page
│   │   │   ├── [id]/                 # Dynamic analysis results
│   │   │   │   └── page.tsx          # Analysis results page
│   │   │   └── loading.tsx           # Analysis loading UI
│   │   ├── reports/                  # Reports pages
│   │   │   ├── page.tsx              # Reports listing
│   │   │   └── loading.tsx           # Reports loading UI
│   │   ├── profile/                  # User profile pages
│   │   │   ├── page.tsx              # User profile
│   │   │   └── loading.tsx           # Profile loading UI
│   │   └── settings/                 # Settings pages
│   │       ├── page.tsx              # User settings
│   │       └── loading.tsx           # Settings loading UI
│   ├── components/                   # Shared + feature-specific components
│   │   ├── ui/                       # Base UI components (shadcn/ui)
│   │   ├── clusters/                 # Cluster visualization suite
│   │   │   ├── ClusterRadarChart.tsx
│   │   │   ├── ClusterConnectionMap.tsx
│   │   │   └── ClusterInsightPanel.tsx
│   │   ├── biomarkers/               # Biomarker visualization components
│   │   │   ├── HolographicGauge.tsx
│   │   │   ├── BiomarkerGrid.tsx
│   │   │   └── BiomarkerTrendPanel.tsx
│   │   ├── insights/                 # Insight delivery system
│   │   │   ├── InsightCard.tsx
│   │   │   ├── ActionableRecommendation.tsx
│   │   │   └── ProgressTracker.tsx
│   │   ├── pipeline/                 # User upload-to-results pipeline
│   │   │   └── AnalysisPipeline.tsx
│   │   ├── forms/                    # Form components
│   │   │   ├── BiomarkerForm.tsx
│   │   │   ├── UserProfileForm.tsx
│   │   │   └── ReportFilters.tsx
│   │   └── layout/                   # Layout components
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── Footer.tsx
│   ├── styles/                       # Tailwind config and design tokens
│   │   ├── globals.css               # Global styles
│   │   ├── components.css            # Component-specific styles
│   │   ├── tailwind.config.ts        # Tailwind CSS configuration
│   │   └── themes/                   # Theme definitions
│   │       ├── light.css
│   │       └── dark.css
│   ├── state/                        # Zustand stores
│   │   ├── authStore.ts              # Authentication state
│   │   ├── analysisStore.ts          # Analysis state
│   │   ├── clusterStore.ts           # Cluster interactions
│   │   └── uiStore.ts                # UI state
│   ├── queries/                      # TanStack Query hooks
│   │   ├── auth.ts                   # Authentication queries
│   │   ├── analysis.ts               # Analysis data queries
│   │   ├── reports.ts                # Reports data queries
│   │   └── user.ts                   # User data queries
│   ├── lib/                          # Frontend utilities
│   │   ├── api.ts                    # Base API client
│   │   ├── auth.ts                   # Authentication utilities
│   │   ├── formatters.ts             # Data formatting
│   │   ├── validators.ts             # Form validation
│   │   ├── constants.ts              # Application constants
│   │   └── utils.ts                  # General utilities
│   ├── types/                        # TypeScript type definitions
│   │   ├── api.ts                    # API response types
│   │   ├── analysis.ts               # Analysis data types
│   │   ├── user.ts                   # User data types
│   │   └── common.ts                 # Common types
│   ├── public/                       # Static assets
│   │   ├── favicon.ico
│   │   ├── robots.txt
│   │   └── assets/                   # Static images and icons
│   │       ├── logos/
│   │       ├── medical-icons/
│   │       └── backgrounds/
│   ├── tests/                        # Jest + RTL tests
│   │   ├── components/               # Component tests
│   │   ├── app/                      # App Router page tests
│   │   ├── queries/                  # Query hook tests
│   │   ├── state/                    # Store tests
│   │   └── utils/                    # Utility tests
│   ├── .storybook/                   # Storybook configuration
│   │   ├── main.ts                   # Storybook main config
│   │   ├── preview.ts                # Storybook preview config
│   │   └── stories/                  # Component stories
│   ├── package.json                  # Node.js dependencies
│   ├── package-lock.json             # Dependency lock file
│   ├── next.config.js                # Next.js configuration
│   ├── tailwind.config.ts            # Tailwind CSS configuration
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── eslint.config.js              # ESLint configuration
│   └── README.md                     # Frontend architecture overview
├── docs/                             # Project documentation
│   ├── context/                      # Context engineering files
│   │   ├── PRD.md                    # Product Requirements Document
│   │   ├── IMPLEMENTATION_PLAN.md    # Development phases and tasks
│   │   ├── PROJECT_STRUCTURE.md      # This file - repository layout
│   │   ├── UX_UI_GUIDE.md            # Design system and UI guidelines
│   │   ├── BUG_TRACKER.md            # Known issues and bug tracking
│   │   ├── STACK_BACKEND.md          # Backend technology decisions
│   │   ├── STACK_FRONTEND.md         # Frontend technology decisions
│   │   ├── STACK_DATABASE.md         # Database technology decisions
│   │   ├── STACK_TOOLS.md            # Development tools and decisions
│   │   ├── WORKFLOW_RULE.md          # AI agent workflow rules
│   │   └── README.md                 # Context documentation index
│   ├── RULES/                        # AI agent rule definitions
│   │   └── GENERATE_RULE.md          # Context generation rules
│   ├── api/                          # API documentation
│   │   ├── openapi.yaml              # OpenAPI specification
│   │   └── endpoints/                # Endpoint documentation
│   ├── architecture/                 # System architecture docs
│   │   ├── overview.md               # System overview
│   │   ├── data-flow.md              # Data flow diagrams
│   │   └── deployment.md             # Deployment architecture
│   ├── user-guide/                   # User documentation
│   │   ├── getting-started.md        # Getting started guide
│   │   ├── analysis-guide.md         # How to use analysis features
│   │   └── reports-guide.md          # How to interpret reports
│   └── development/                  # Developer documentation
│       ├── setup.md                  # Development setup
│       ├── contributing.md           # Contribution guidelines
│       └── testing.md                # Testing guidelines
├── ops/                              # Operations and deployment
│   ├── docker/                       # Docker configurations
│   │   ├── Dockerfile.backend        # Backend container
│   │   ├── Dockerfile.frontend       # Frontend container
│   │   └── docker-compose.yml        # Multi-container setup
│   ├── kubernetes/                   # Kubernetes manifests
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   └── ingress.yaml
│   ├── terraform/                    # Infrastructure as Code
│   │   ├── main.tf                   # Main infrastructure
│   │   ├── variables.tf              # Variable definitions
│   │   └── outputs.tf                # Output definitions
│   ├── scripts/                      # Deployment scripts
│   │   ├── deploy.sh                 # Deployment script
│   │   ├── backup.sh                 # Backup script
│   │   └── health-check.sh           # Health monitoring script
│   └── monitoring/                   # Monitoring configurations
│       ├── prometheus.yml            # Prometheus configuration
│       ├── grafana/                  # Grafana dashboards
│       └── alerts.yml                # Alert rules
├── .github/                          # GitHub workflows and templates
│   ├── workflows/                    # CI/CD workflows
│   │   ├── ci.yml                    # Continuous Integration
│   │   ├── cd.yml                    # Continuous Deployment
│   │   └── security.yml              # Security scanning
│   └── ISSUE_TEMPLATE/               # Issue templates
├── .env                              # Environment variables (uncommitted - contains secrets)
├── .env.example                      # Environment variables template (committed)
├── .gitignore                        # Git ignore rules (protects sensitive keys)
├── LICENSE.txt                       # Project license
├── README.md                         # Project overview and setup
└── healthiq-code.txt                 # Legacy code reference
```

## Planned Structure (Full System Vision)

This blueprint represents the complete architectural vision for HealthIQ AI v5, including:

> **⚠️ Frontend Architecture Note**: The `frontend/` structure above reflects our **planned Next.js 14+ App Router architecture**. The initial build will follow this structure, replacing the current Vite + React Router setup. This is our **canonical frontend architecture** for Sprint 1 and beyond.

### Key Architectural Principles

- **Canonical Repo Location**: [HealthIQ-AI-v5 on GitHub](https://github.com/abroad1/HealthIQ-AI-v5)
- **Branching & Backup**: Feature branches must be used for major changes. Forks are permitted but must retain context metadata and alignment with `PROJECT_STRUCTURE.md`.
- **Monorepo Structure**: Single repository containing all components for easier development and deployment
- **Clear Separation**: Backend (API), Frontend (UI), and Operations (Infrastructure) are clearly separated
- **Domain-Driven Design**: Backend organized by business domains (models, pipeline, insights, etc.)
- **Component-Based Frontend**: Reusable UI components with clear separation of concerns
- **Comprehensive Documentation**: Context engineering files for AI agent guidance
- **Infrastructure as Code**: All deployment and infrastructure configurations versioned
- **Testing Strategy**: Comprehensive test coverage across all layers

### Implementation Status

- **✅ Currently Implemented**: Core backend structure, basic frontend, essential documentation
- **🔄 In Progress**: Pipeline orchestration, insight engines, cluster algorithms
- **📋 Planned**: Full services layer, comprehensive testing, deployment infrastructure
- **🔮 Future**: Advanced integrations, clinical-grade features, enterprise capabilities
