/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: { domains: [process.env.NEXT_PUBLIC_HOSTNAME], unoptimized: true },
  assetPrefix: '/sd/static',
};

module.exports = nextConfig;
