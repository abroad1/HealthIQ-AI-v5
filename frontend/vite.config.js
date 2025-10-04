// Placeholder Vite config for Lovable preview tooling.
// This project uses Next.js (no Vite build). This file exists to satisfy
// environment checks and is not used by the app.
// Required by Lovable preview: server must run on port 8080.

import { componentTagger } from "lovable-tagger";

export default ({ mode }) => ({
  server: {
    host: "::",
    port: 8080,
  },
  plugins: [
    mode === 'development' && componentTagger(),
  ].filter(Boolean),
});
