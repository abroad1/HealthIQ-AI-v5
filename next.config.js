/** @type {import('next').NextConfig} */
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
}

module.exports = nextConfig
