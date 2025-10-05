/** @type {import('next').NextConfig} */
const path = require('node:path')

const nextConfig = {
  // Prevent Next.js from treating our Vite React Router files in src/pages as Next pages
  // by restricting recognized page extensions to a non-existent extension.
  pageExtensions: ["page.mdx"],
  
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
  webpack: (config) => {
    config.resolve = config.resolve || {}
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      '@': path.resolve(__dirname, './app'),
    }
    return config
  },
}

module.exports = nextConfig
