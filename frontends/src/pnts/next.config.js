/** @type {import('next').NextConfig} */

const nextConfig = {
  basePath: '', // 设置应用程序的路径前缀，用于在域的子路径下部署应用程序时
  compress: false, // 压缩渲染内容和静态文件，一般在 nginx 等代理上启用 gzip
  // 编译指示器位置
  devIndicators: {
    buildActivityPosition: 'bottom-right',
    buildActivity: true, // 关闭提示
  },
  distDir: './release/next/build', // 用于自定义构建目录的名称，默认为 .next
  // env: {}, // 环境变量
  eslint: {
    // 警告： 这样即使项目出现 ESLint 错误，也能成功完成生产构建。
    ignoreDuringBuilds: false,
  },
  modularizeImports: {
    '@mui/material': {
      transform: '@mui/material/{{member}}',
    },
    '@mui/lab': {
      transform: '@mui/lab/{{member}}',
    },
  },
  // output: 'export',
  trailingSlash: false, // 将带有尾部斜杠的 URL 重定向到不带尾部斜杠的对应 URL
  // 自动转换和捆绑来自本地包或外部依赖项的依赖项
  // transpilePackages: [],
  typescript: {
    ignoreBuildErrors: false, // 生产构建时，忽略项目中存在的 TypeScript 错误
  },
  webpack: (config, options) => {
    // Grab the existing rule that handles SVG imports
    const fileLoaderRule = config.module.rules.find((rule) =>
      rule.test?.test?.('.svg'),
    )

    config.module.rules.push(
      // Reapply the existing rule, but only for svg imports ending in ?url
      {
        ...fileLoaderRule,
        test: /\.svg$/i,
        resourceQuery: /url/, // *.svg?url
      },
      // Convert all other *.svg imports to React components
      {
        test: /\.svg$/i,
        issuer: /\.[jt]sx?$/,
        resourceQuery: { not: /url/ }, // exclude if *.svg?url
        use: ['@svgr/webpack'],
      },
    );

    // Modify the file loader rule to ignore *.svg, since we have it handled now.
    fileLoaderRule.exclude = /\.svg$/i

    return config;
  },
  // 体验功能
  experimental: {},
};

module.exports = nextConfig;
