# HealthIQ AI v5 Frontend

Next.js 14+ App Router frontend for the HealthIQ AI v5 platform.

## Architecture

- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: Zustand stores
- **TypeScript**: Full type safety
- **Storybook**: Component documentation and testing

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run Storybook
npm run storybook
```

## Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Project Structure

```
app/
├── components/          # React components
│   ├── clusters/       # Cluster visualization components
│   ├── biomarkers/     # Biomarker chart components
│   ├── insights/       # AI insights components
│   └── pipeline/       # Analysis pipeline components
├── services/           # API service layer
├── state/             # Zustand stores
├── types/             # TypeScript type definitions
├── styles/            # Tailwind configuration
└── lib/               # Utility functions and API client
```
