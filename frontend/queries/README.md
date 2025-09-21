# TanStack Query Hooks

This directory contains TanStack Query hooks for server-side data management in HealthIQ AI v5.

## Query Structure

### `auth.ts`
Authentication-related queries and mutations.

**Queries:**
- `useUser()` - Get current user profile
- `useAuthStatus()` - Check authentication status

**Mutations:**
- `useLogin()` - User login
- `useLogout()` - User logout
- `useRegister()` - User registration

### `analysis.ts`
Analysis-related queries and mutations.

**Queries:**
- `useAnalysis(analysisId)` - Get analysis by ID
- `useAnalysisList()` - Get user's analysis history
- `useAnalysisProgress(analysisId)` - Get real-time progress

**Mutations:**
- `useCreateAnalysis()` - Start new analysis
- `useUploadFile()` - Upload biomarker data

### `reports.ts`
Report generation and management queries.

**Queries:**
- `useReport(reportId)` - Get generated report
- `useReportList()` - Get user's reports

**Mutations:**
- `useGenerateReport()` - Generate new report
- `useExportReport()` - Export report in various formats

### `user.ts`
User profile and preferences queries.

**Queries:**
- `useUserProfile()` - Get user profile
- `useUserPreferences()` - Get user settings

**Mutations:**
- `useUpdateProfile()` - Update user profile
- `useUpdatePreferences()` - Update user settings

## Usage Guidelines

1. **Use proper query keys** - Follow consistent naming patterns
2. **Handle loading states** - Provide proper loading indicators
3. **Implement error handling** - Show meaningful error messages
4. **Optimize caching** - Use appropriate stale times
5. **Invalidate properly** - Update related queries when data changes
