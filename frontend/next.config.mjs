/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    disableStaticImages: true, // Disable default handling of static images
  },
  webpack(config) {
    config.module.rules.push({
      test: /\.(png|jpe?g|gif|svg)$/i,
      type: "asset/resource",
    });
    return config;
  },
  sassOptions: {
    implementation: "sass-embedded",
  },
};

export default nextConfig;
