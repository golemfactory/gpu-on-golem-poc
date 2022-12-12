/** @type {import('next').NextConfig} */

const isLukaszServer = process.env.APP_ENV === 'lukasz-biuro'

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: { domains: [process.env.NEXT_PUBLIC_HOSTNAME], unoptimized: true },
  assetPrefix: isLukaszServer ? '/sd/static' : undefined,
};

module.exports = nextConfig;
