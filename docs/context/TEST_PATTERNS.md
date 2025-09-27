# 🧪 Value-First Test Patterns & Templates

**Document Type**: Level 2 – Canonical Specification  
**Purpose**: Defines value-first test patterns, templates, and best practices for HealthIQ AI v5.  
**Authority**: This document provides reusable templates and patterns for business-value focused test implementation.

---

## 📋 Table of Contents

1. [Value-First Testing Patterns](#value-first-testing-patterns)
2. [High-Value Test Templates](#high-value-test-templates)
3. [Business Logic Test Templates](#business-logic-test-templates)
4. [API Integration Test Templates](#api-integration-test-templates)
5. [Error Scenario Test Templates](#error-scenario-test-templates)
6. [Test Quality Checklist](#test-quality-checklist)
7. [Test Justification Template](#test-justification-template)

---

## 🎯 Value-First Testing Patterns

### Test-Alongside Development Approach

```typescript
// 1. Identify business value first
// What user scenario does this test cover?
// What business-critical functionality does it validate?

// 2. Write test for business logic
describe('AnalysisService - Core User Workflow', () => {
  it('should complete analysis workflow for user', async () => {
    // Test the complete user journey, not implementation details
    const result = await analysisService.processUserAnalysis(userData);
    expect(result.status).toBe('completed');
    expect(result.insights).toBeDefined();
  });
});

// 3. Implement business logic
class AnalysisService {
  async processUserAnalysis(userData: UserData): Promise<AnalysisResult> {
    // Business-critical implementation
    return this.orchestrateAnalysis(userData);
  }
}
```

### High-Value Test File Structure

```
frontend/app/
├── services/
│   ├── analysis.ts          # Implementation
│   └── analysis.test.ts     # High-value tests only
├── state/
│   ├── analysisStore.ts     # Implementation  
│   └── analysisStore.test.ts # Business logic tests
└── components/
    ├── AnalysisPanel.tsx    # Implementation
    └── AnalysisPanel.test.tsx # User workflow tests only
```

---

## 🔧 High-Value Test Templates

### Business Logic Test Template

```typescript
// state/analysisStore.test.ts
import { useAnalysisStore } from './analysisStore';

describe('AnalysisStore - Business Logic', () => {
  beforeEach(() => {
    useAnalysisStore.getState().clearAnalysis();
  });

  describe('Core User Workflow', () => {
    it('should maintain analysis state consistency during user workflow', () => {
      // Test business-critical state management
      const store = useAnalysisStore.getState();
      
      // User starts analysis
      store.setCurrentAnalysis({ id: '123', status: 'processing' });
      expect(store.currentAnalysis?.status).toBe('processing');
      
      // User gets results
      store.setCurrentAnalysis({ id: '123', status: 'completed', results: {} });
      expect(store.isAnalysisComplete()).toBe(true);
    });

    it('should handle analysis errors gracefully', () => {
      // Test critical error handling
      const store = useAnalysisStore.getState();
      store.setError({ message: 'Analysis failed', code: 'ANALYSIS_ERROR' });
      
      expect(store.error).toBeDefined();
      expect(store.isLoading).toBe(false);
    });
  });
});
```

### API Integration Test Template

```typescript
// services/analysis.test.ts
import { AnalysisService } from './analysis';

describe('AnalysisService - API Integration', () => {
  let service: AnalysisService;
  let mockFetch: jest.MockedFunction<typeof fetch>;

  beforeEach(() => {
    service = new AnalysisService();
    mockFetch = global.fetch as jest.MockedFunction<typeof fetch>;
    jest.clearAllMocks();
  });

  describe('Critical API Workflows', () => {
    it('should handle successful analysis API call', async () => {
      // Test business-critical API integration
      const mockResponse = { analysisId: '123', status: 'started' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await service.startAnalysis({
        biomarkers: [{ name: 'glucose', value: 5.2 }],
        userProfile: { age: 35, sex: 'male' }
      });

      expect(result.success).toBe(true);
      expect(result.data.analysisId).toBe('123');
    });

    it('should handle API errors gracefully', async () => {
      // Test critical error handling
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ error: 'Server error' }),
      } as Response);

      const result = await service.startAnalysis({
        biomarkers: [],
        userProfile: { age: 35, sex: 'male' }
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Server error');
    });
  });
});
```

### Backend Business Logic Test Template

```python
# tests/unit/test_analysis_service.py
import pytest
from core.services.analysis_service import AnalysisService

class TestAnalysisService:
    """Test business-critical analysis functionality."""
    
    def test_complete_analysis_workflow(self):
        """Test the complete user analysis workflow."""
        # Test business-critical workflow
        service = AnalysisService()
        user_data = {
            'biomarkers': [{'name': 'glucose', 'value': 5.2}],
            'user_profile': {'age': 35, 'sex': 'male'}
        }
        
        result = service.process_analysis(user_data)
        
        assert result.status == 'completed'
        assert result.insights is not None
        assert result.clusters is not None
    
    def test_handles_invalid_biomarker_data(self):
        """Test critical error handling for invalid data."""
        service = AnalysisService()
        invalid_data = {
            'biomarkers': [{'name': 'invalid', 'value': -1}],
            'user_profile': {'age': -5, 'sex': 'invalid'}
        }
        
        with pytest.raises(ValueError, match="Invalid biomarker data"):
            service.process_analysis(invalid_data)
```

---

## 🚫 What NOT to Test (Low-Value Tests)

### Framework Behavior (Don't Test)
```typescript
// ❌ DON'T TEST - Framework behavior
describe('Pydantic Validation', () => {
  it('should validate required fields', () => {
    // This is testing Pydantic, not our business logic
  });
});

// ❌ DON'T TEST - Basic rendering
describe('Component Rendering', () => {
  it('should render without crashing', () => {
    // This is testing React, not our business logic
  });
});
```

### Trivial Functions (Don't Test)
```typescript
// ❌ DON'T TEST - Trivial functions
describe('Math Utils', () => {
  it('should add two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});

// ❌ DON'T TEST - String formatting
describe('String Utils', () => {
  it('should format date string', () => {
    expect(formatDate('2025-01-27')).toBe('Jan 27, 2025');
  });
});
```

---

## ✅ Test Quality Checklist

Before writing any test, ask:

1. **Business Value**: Does this test prevent user pain or catch business-critical bugs?
2. **User Scenario**: What real user scenario does this test cover?
3. **Failure Impact**: What happens if this test fails? Is it critical?
4. **Maintenance Cost**: Is this test easy to understand and modify?
5. **Justification**: Would I delete this test if it broke? If yes, don't write it.

### Test Justification Template

```markdown
## Test: test_user_gets_analysis_results

**User Scenario**: User uploads biomarkers and receives analysis
**Business Value**: Core product functionality - users can't get results without this
**Failure Impact**: Users can't get analysis results (critical business failure)
**Maintenance Cost**: Low (stable API, clear test purpose)
**Justification**: ✅ KEEP - Essential for core product value
```

---

## 🎯 Error Scenario Testing

### Critical Error Handling Tests

```typescript
describe('Critical Error Scenarios', () => {
  it('should handle network failures gracefully', async () => {
    // Test critical error handling
    mockFetch.mockRejectedValueOnce(new Error('Network error'));
    
    const result = await service.startAnalysis(validData);
    
    expect(result.success).toBe(false);
    expect(result.error).toBe('Network error');
    expect(uiStore.getState().error).toBeDefined();
  });

  it('should handle invalid user data', async () => {
    // Test data validation
    const result = await service.startAnalysis({
      biomarkers: [],
      userProfile: { age: -1, sex: 'invalid' }
    });
    
    expect(result.success).toBe(false);
    expect(result.error).toContain('Invalid user data');
  });
});
```

---

## 📊 Test Documentation Standards

### High-Value Test Documentation

```typescript
/**
 * Test: Analysis Service - Core User Workflow
 * 
 * Business Value: Ensures users can complete the primary product workflow
 * User Scenario: User uploads biomarkers → gets analysis → views results
 * Failure Impact: Users cannot get analysis results (critical business failure)
 * Maintenance Cost: Low (stable API, clear business logic)
 */
describe('AnalysisService - Core User Workflow', () => {
  // Test implementation
});
```

### Test Results Documentation

```markdown
## High-Value Test Results

### Backend Tests
- **File**: `test_analysis_service.py`
- **Purpose**: Core business logic - analysis orchestration
- **Run Command**: `pytest backend/tests/unit/test_analysis_service.py -v`
- **Last Result**: 14 passed, 0 failed
- **Business Value**: Ensures analysis pipeline works correctly

### Frontend Tests
- **File**: `analysisStore.test.ts`
- **Purpose**: Core business logic - analysis state management
- **Run Command**: `npm test -- analysisStore.test.ts`
- **Last Result**: 15 passed, 0 failed
- **Business Value**: Ensures analysis state consistency across UI
```

---

## 🔄 Test Maintenance Guidelines

### When to Archive Tests
- Test fails because underlying code was intentionally removed
- Test validates functionality replaced by new modules
- Test contains mocks referencing deprecated APIs
- Test is redundant with newer test suites

### When to Delete Tests
- Test is pure coverage padding
- Test validates framework behavior
- Test is trivial (math operations, string formatting)
- Test duplicates other tests

### Archive Template
```typescript
// ARCHIVED TEST
// Reason: Medium-value test (infrastructure test, not user-facing)
// Archived: 2025-01-27
// Original Path: frontend/tests/services/auth.test.ts

// Original test content...
```

---

**Remember: We test for business value, not for testing's sake. Every test must have a clear purpose: preventing user pain or catching business-critical bugs.**