# 🎨 UX / UI Guidelines

> This document defines the visual language, layout principles, and interaction patterns that govern the HealthIQ-AI v5 frontend. Our frontend is built using **Next.js 14+ (React 18)**, TypeScript, Tailwind CSS, and a modular component system built around design tokens. The app leverages shadcn/ui, Radix primitives, and Framer Motion to deliver a modern, accessible, and responsive medical-grade UX.

---

## 🧭 Design Principles

| Principle | Description |
|----------|-------------|
| **Clinical Clarity** | No clutter, jargon-free, results must be easy to understand |
| **Futuristic Elegance** | Holographic, Function Health–inspired UI with glow effects and transparency |
| **Immersive Storytelling** | Scroll-based animations reveal insights like a narrative journey |
| **User Empowerment** | Encourage action through beautifully designed CTA panels |
| **Accessibility First** | Font sizing, contrast, motion sensitivity respected |

---

## ⚙️ Tech Stack

- **Next.js 14+** (React 18) with TypeScript
- **Tailwind CSS** with semantic design tokens
- **Radix UI** components for accessibility
- **Framer Motion** for animations
- **Lucide React** for icons
- **Next.js App Router** for navigation

---

## 🌓 Theme System

### Light/Dark Mode Support
- Uses `data-theme` attribute system
- Default is dark mode: `[data-theme="dark"]`
- Toggle available via `useTheme()` hook

---

## 🎨 Semantic Color Tokens

All tokens use HSL format for theme consistency.

### Core
```css
--background, --foreground
--primary, --primary-foreground
--secondary, --secondary-foreground
```

### UI Elements
```css
--card, --card-foreground
--popover, --popover-foreground
--muted, --muted-foreground
--border, --input, --ring
```

### Health-Specific
```css
--health-excellent, --health-good
--health-fair, --health-poor
--health-critical
```

### Gradients & Shadows
```css
--gradient-health, --gradient-card, --gradient-primary
--shadow-health, --shadow-card, --shadow-glow
```

---

## 🔤 Typography

### Hierarchy
```tsx
H1: text-4xl font-bold
H2: text-2xl font-semibold
H3: text-lg font-medium
Body: text-base
Caption: text-sm text-muted-foreground
```

Font: Inter (fallback: system sans-serif)

---

## 📐 Spacing System

### Containers
- Max width: 1400px at 2xl
- Padding: `px-8` default

### Component Gaps
- Section spacing: `space-y-8`
- Card padding: `p-6`
- Button: `px-4 py-2`
- Grid gaps: `gap-6`

---

## 🧱 Component System

### Core Atoms (from shadcn/ui)
- `Button`, `Card`, `Label`, `Input`, `Toast`, `Dialog`

### Biomarker Components
- `HolographicGauge.tsx`
- `BiomarkerGrid.tsx`
- `TrendLine.tsx`
- `RangeBand.tsx`

### Cluster Components
- `ClusterRadarChart.tsx`
- `ClusterConnectionMap.tsx`
- `ClusterNarrativePanel.tsx`

### Insight Delivery
- `InsightCard.tsx`
- `ActionableRecommendation.tsx`
- `LifestyleSummary.tsx`

### Shared
- `ScrollRevealWrapper.tsx`
- `AnimatedCounter.tsx`
- `SectionDivider.tsx`
- `Navigation.tsx`, `Tabs`, `TabsList`, `TabsTrigger`

---

## 📄 Page Structure

### `/upload`
- Upload UI + questionnaire
- Placeholder for parsed preview

### `/results`
- Summary → Cluster View → Marker Detail → Recommendations

### `/about`, `/tech`, `/contact`
- Reuse shared hero + CTA components

---

## 🧭 Interaction Patterns

- Scroll animation: `FadeInUp`, `RevealLeft`, `ParallaxSection`
- Framer Motion custom transitions
- Toggle views, accordion panels, tabs
- Loading and error states

---

## 🔍 Accessibility

- Radix UI foundation for dialogs, alerts, tooltips
- Keyboard-accessible, semantic HTML, ARIA support
- Contrast compliant (AA minimum)

---

## 📱 Responsive Design

### Breakpoints
```css
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1400px (max container)
```

- Mobile-first layout
- Responsive grid with Tailwind utilities

---

## 📊 Health Analytics UX

### Visualisation
- Health tokens to show state (e.g. text-health-critical)
- Consistent chart legends and units

### Biomarker Cards
- Sorted and grouped by function
- Reference ranges visible
- Critical markers flagged

---

## 🔮 Future Enhancements

- Dark mode (available now)
- Theme presets per persona
- Real-time biomarker animation effects
- Lottie illustrations for storytelling
- Insight video/voice narration (LLM integration)

---

These guidelines reflect best practices from Loveable.dev’s design system and are now fully integrated into HealthIQ-AI’s UI strategy.

