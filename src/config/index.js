/**
 * 环境配置
 */
export const ENV = {
  development: 'development',
  production: 'production',
};

/**
 * 当前环境
 */
export const CURRENT_ENV = process.env.NODE_ENV || ENV.development;

/**
 * API 基础配置
 */
export const API_CONFIG = {
  development: {
    baseUrl: 'http://127.0.0.1:5000',
  },
  production: {
    baseUrl: 'https://api.example.com', // 生产环境 API 地址
  },
};

/**
 * API 基础 URL
 */
export const API_BASE_URL = API_CONFIG[CURRENT_ENV].baseUrl;