import { API_BASE_URL } from '@/config';

/**
 * 解析API响应错误
 * @param {Response} response 响应对象
 * @returns {Promise<Error>} 错误对象
 */
const parseApiError = async (response) => {
  let errorMessage = `HTTP ${response.status}`;
  let errorDetails = null;
  
  try {
    const data = await response.json();
    if (data.error) {
      errorMessage = data.error;
    } else if (data.message) {
      errorMessage = data.message;
    }
    if (data.details) {
      errorDetails = data.details;
    }
  } catch (e) {
    // 如果无法解析JSON，使用状态文本
    errorMessage = response.statusText || errorMessage;
  }
  
  const error = new Error(errorMessage);
  error.status = response.status;
  error.details = errorDetails;
  return error;
};

/**
 * 监控服务相关的 API 服务
 */
export const MonitorService = {
  /**
   * 获取监控服务状态
   * @returns {Promise<Object>} 监控状态信息
   */
  async getStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/monitor/status`);
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '获取监控状态失败');
        error.details = data.details;
        throw error;
      }
      return data.data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        const networkError = new Error('网络连接失败，请检查网络连接');
        networkError.code = 'NETWORK_ERROR';
        throw networkError;
      }
      throw error;
    }
  },

  /**
   * 启动监控服务
   * @returns {Promise<Object>} 启动结果
   */
  async start() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/monitor/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '启动监控服务失败');
        error.details = data.details;
        throw error;
      }
      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        const networkError = new Error('网络连接失败，请检查网络连接');
        networkError.code = 'NETWORK_ERROR';
        throw networkError;
      }
      throw error;
    }
  },

  /**
   * 停止监控服务
   * @returns {Promise<Object>} 停止结果
   */
  async stop() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/monitor/stop`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '停止监控服务失败');
        error.details = data.details;
        throw error;
      }
      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        const networkError = new Error('网络连接失败，请检查网络连接');
        networkError.code = 'NETWORK_ERROR';
        throw networkError;
      }
      throw error;
    }
  },
};

export default MonitorService; 