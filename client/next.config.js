const { withSentryConfig } = require('@sentry/nextjs');

/** @type {import('next').NextConfig} */

const serverAssetPrefix = {
  'lukasz-biuro': '/sd/static',
  'gpu.dev-test.golem.network': '/static',
};

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: { domains: [process.env.NEXT_PUBLIC_HOSTNAME], unoptimized: true },
  assetPrefix: serverAssetPrefix[process.env.APP_ENV],
};

module.exports = nextConfig;

module.exports = withSentryConfig(module.exports, { silent: true }, { hideSourcemaps: true });
