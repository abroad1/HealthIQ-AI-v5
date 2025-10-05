// Ambient module declarations to satisfy TypeScript when scanning non-Next files.
// This prevents Next's type checker from failing on Vite-only alias imports under src/ that use "@/".
// Note: Runtime resolution for these is handled by Vite; Next does not import those files.
declare module '@/!*';
