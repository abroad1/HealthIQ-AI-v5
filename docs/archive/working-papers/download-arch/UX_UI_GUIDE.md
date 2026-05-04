# HealthIQ UX/UI Design Guide

## Tech Stack
- **React 18** with TypeScript
- **Tailwind CSS** with semantic design tokens
- **Radix UI** components for accessibility
- **Framer Motion** for animations
- **Lucide React** for icons
- **React Router** for navigation

## Theme System

### Light/Dark Mode Support
Our application supports both light and dark themes using the `data-theme` attribute system:
- **Light Theme**: `[data-theme="light"]`
- **Dark Theme**: `[data-theme="dark"]` (default)
- **Theme Toggle**: Available via `useTheme()` hook from `ThemeContext`

## Color System

### Semantic Color Tokens
Always use semantic color tokens instead of direct colors. All colors use HSL format for better theme consistency.

#### Primary Colors
```css
--background: Main background color
--foreground: Main text color
--primary: Brand primary color (teal/cyan)
--primary-foreground: Text on primary background
--secondary: Secondary accent color
--secondary-foreground: Text on secondary background
```

#### UI Element Colors
```css
--card: Card background
--card-foreground: Card text
--popover: Popover background
--popover-foreground: Popover text
--muted: Muted background
--muted-foreground: Muted text
--border: Border color
--input: Input border color
--ring: Focus ring color
```

#### Health-Specific Colors
```css
--health-excellent: Green tones for excellent health scores
--health-good: Light green for good health scores
--health-fair: Yellow/amber for fair health scores
--health-poor: Orange for poor health scores
--health-critical: Red for critical health scores
```

#### Usage Examples
```tsx
// ✅ Correct - Use semantic tokens
<div className="bg-card text-card-foreground border border-border">
<Button variant="primary" className="text-primary-foreground">
<div className="text-health-excellent">Excellent Score</div>

// ❌ Wrong - Don't use direct colors
<div className="bg-white text-black border-gray-200">
<Button className="bg-blue-500 text-white">
<div className="text-green-500">Excellent Score</div>
```

## Gradients & Effects

### Available Gradients
```css
--gradient-health: Health status gradient
--gradient-card: Card background gradient
--gradient-primary: Primary brand gradient
```

### Shadow System
```css
--shadow-health: Health component shadows
--shadow-card: Card shadows
--shadow-glow: Glowing effects
```

### Usage
```tsx
<div className="bg-gradient-health shadow-health">
<Card className="bg-gradient-card shadow-card">
```

## Spacing System

### Container Spacing
- **Container**: Centered with 2rem padding
- **Max Width**: 1400px on 2xl screens
- **Responsive**: Automatic padding adjustment

### Component Spacing
- **Section Gaps**: `space-y-8` (2rem vertical spacing)
- **Card Padding**: `p-6` (1.5rem all sides)
- **Button Padding**: `px-4 py-2` for default size
- **Grid Gaps**: `gap-6` for component grids

## Typography

### Hierarchy
- **H1**: `text-4xl font-bold` - Page titles
- **H2**: `text-2xl font-semibold` - Section headers
- **H3**: `text-lg font-medium` - Subsection headers
- **Body**: `text-base` - Default body text
- **Caption**: `text-sm text-muted-foreground` - Secondary text

### Usage Examples
```tsx
<h1 className="text-4xl font-bold text-foreground">HealthIQ Dashboard</h1>
<h2 className="text-2xl font-semibold text-foreground">Biomarkers</h2>
<p className="text-base text-muted-foreground">Analysis summary</p>
```

## Component Guidelines

### Cards
Use the `Card` component from our UI library:
```tsx
<Card className="p-6 bg-gradient-card border-border shadow-card">
  <CardHeader>
    <CardTitle>Health Score</CardTitle>
  </CardHeader>
  <CardContent>
    {/* Card content */}
  </CardContent>
</Card>
```

### Buttons
Use semantic button variants:
```tsx
<Button variant="default">Primary Action</Button>
<Button variant="secondary">Secondary Action</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="ghost">Ghost Button</Button>
```

### Health Indicators
Use health-specific color tokens for scores and statuses:
```tsx
<div className="text-health-excellent">95% - Excellent</div>
<div className="text-health-good">78% - Good</div>
<div className="text-health-fair">65% - Fair</div>
<div className="text-health-poor">45% - Poor</div>
<div className="text-health-critical">25% - Critical</div>
```

### Navigation
Use consistent navigation patterns:
```tsx
<Navigation /> // Global navigation component
<Tabs defaultValue="overview">
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="biomarkers">Biomarkers</TabsTrigger>
  </TabsList>
</Tabs>
```

## Animation Guidelines

### Smooth Transitions
Use the custom transition timing functions:
```css
transition-timing-function: var(--transition-smooth)
transition-timing-function: var(--transition-bounce)
```

### Available Animations
```tsx
// Accordion animations (built-in)
<Accordion /> // Automatically uses accordion-up/down

// Framer Motion for complex animations
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
```

## Accessibility

### Standards
- All interactive elements must be keyboard accessible
- Use semantic HTML elements
- Maintain proper color contrast ratios
- Include proper ARIA labels and descriptions

### Implementation
```tsx
// Use Radix UI components for built-in accessibility
<Dialog>
<AlertDialog>
<Tooltip>
<Select>

// Always include proper labeling
<Button aria-label="Close dialog">
<Input aria-describedby="error-message">
```

## Responsive Design

### Breakpoints
```css
sm: '640px'
md: '768px'  
lg: '1024px'
xl: '1280px'
2xl: '1400px' (container max-width)
```

### Mobile-First Approach
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
<div className="text-sm md:text-base lg:text-lg">
```

## Best Practices

### Do's
- ✅ Use semantic color tokens from the design system
- ✅ Maintain consistent spacing with Tailwind utilities
- ✅ Support both light and dark themes
- ✅ Use TypeScript for type safety
- ✅ Follow the component composition pattern
- ✅ Implement proper loading and error states

### Don'ts
- ❌ Use direct color values (bg-white, text-black, etc.)
- ❌ Override theme colors with custom CSS
- ❌ Mix different spacing systems
- ❌ Ignore accessibility requirements
- ❌ Create components without proper TypeScript types
- ❌ Use animations that reduce performance

## Health Analytics Specific Guidelines

### Data Visualization
- Use health-specific color tokens for different score ranges
- Maintain consistent chart styling across components
- Include proper legends and labels
- Support both light and dark theme variations

### Biomarker Display
- Group related biomarkers logically
- Use consistent units and formatting
- Highlight critical values appropriately
- Provide context with reference ranges

### Dashboard Layout
- Prioritize most important information above the fold
- Use progressive disclosure for detailed data
- Maintain consistent card layouts
- Support various screen sizes and orientations