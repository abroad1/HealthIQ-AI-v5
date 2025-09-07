# HealthIQ-AI v5 Backend

AI-powered biomarker analysis platform backend built with FastAPI and Python 3.11+.

## Features

- **FastAPI Application**: Modern, fast web framework with automatic OpenAPI documentation
- **Immutable Models**: Pydantic v2 models with `frozen=True` and `extra="forbid"`
- **Canonical Boundary**: Single Source of Truth (SSOT) for biomarker definitions
- **Server-Sent Events**: Real-time analysis progress streaming
- **Pipeline Architecture**: Modular analysis orchestration
- **Type Safety**: Full mypy type checking and strict linting

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

### Development Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000/api/
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

All endpoints are prefixed with `/api/`:

- `GET /api/health` - Health check
- `POST /api/analysis/start` - Start biomarker analysis
- `GET /api/analysis/events` - Stream analysis progress (SSE)
- `GET /api/analysis/result` - Get analysis results

## Testing

Run the test suite:

```bash
# Run all tests
pytest -q

# Run with coverage
pytest --cov=app --cov=core --cov-report=html

# Run specific test file
pytest tests/enforcement/test_canonical_only.py -v
```

## Code Quality

### Linting

```bash
# Run ruff linter
ruff check .

# Auto-fix issues
ruff check . --fix
```

### Type Checking

```bash
# Run mypy type checker
mypy .
```

### Formatting

```bash
# Format code with ruff
ruff format .
```

## Architecture

### Core Components

- **`app/`**: FastAPI application and routes
- **`core/`**: Business logic and domain models
  - **`models/`**: Immutable Pydantic models
  - **`canonical/`**: SSOT resolver and normalization
  - **`pipeline/`**: Analysis orchestration and SSE
  - **`insights/`**: Insight generation framework
  - **`clustering/`**: Biomarker clustering engine
  - **`dto/`**: Data transfer object builders
- **`ssot/`**: Single Source of Truth YAML files
- **`tools/`**: Utility scripts
- **`tests/`**: Test suite

### Key Design Principles

1. **Immutable Models**: All Pydantic models use `frozen=True` and `extra="forbid"`
2. **Canonical Enforcement**: Orchestrator validates canonical-only biomarker keys
3. **SSE Streaming**: Real-time analysis progress via Server-Sent Events
4. **Type Safety**: Comprehensive type hints and mypy checking
5. **Separation of Concerns**: Clear boundaries between layers

## Biomarker Data

### SSOT Files

- **`ssot/biomarkers.yaml`**: Canonical biomarker definitions with aliases
- **`ssot/ranges.yaml`**: Reference ranges for different populations
- **`ssot/units.yaml`**: Unit definitions and conversion factors

### Canonical Names

Biomarkers must use canonical names (e.g., `total_cholesterol`, `glucose`, `hdl_cholesterol`). Aliases are automatically mapped to canonical names during normalization.

## Development Tools

### Export OpenAPI Spec

```bash
# Export OpenAPI specification (requires running server)
python tools/export_openapi.py
```

This creates `docs/openapi.yaml` with the complete API specification.

### Project Configuration

- **`pyproject.toml`**: Project metadata, dependencies, and tool configuration
- **`.gitignore`**: Git ignore patterns for Python projects
- **`ruff`**: Fast Python linter with strict rules
- **`mypy`**: Static type checker with strict settings

## Environment Variables

No environment variables are required for basic operation. The application runs with sensible defaults for development.

## Contributing

1. Follow the existing code style and patterns
2. Ensure all tests pass: `pytest -q`
3. Run linting: `ruff check .`
4. Run type checking: `mypy .`
5. Add tests for new functionality
6. Update documentation as needed

## License

MIT License - see LICENSE file for details.
