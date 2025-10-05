/** @type {import('next').NextConfig} */
const nextConfig = {
  
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
    dirs: ['app', 'components', 'lib', 'services', 'state', 'types'],
  },
  // Add cache busting for development
  generateEtags: false,
  poweredByHeader: false,
}

module.exports = nextConfig
