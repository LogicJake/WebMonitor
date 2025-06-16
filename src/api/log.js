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
 * 日志相关的 API 服务
 */
export const LogService = {
  /**
   * 获取监控日志
   * @param {Object} params 查询参数
   * @returns {Promise<Array>} 日志列表
   */
  async getLogs(params = {}) {
    try {
      const queryParams = new URLSearchParams();
      
      if (params.limit) queryParams.append('limit', params.limit);
      if (params.level) queryParams.append('level', params.level);
      if (params.task_id) queryParams.append('task_id', params.task_id);
      
      const url = `${API_BASE_URL}/api/logs${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw await parseApiError(response);
      }
      
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '获取日志失败');
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
   * 获取日志统计信息
   * @returns {Promise<Object>} 统计信息
   */
  async getLogStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/logs/stats`);
      
      if (!response.ok) {
        throw await parseApiError(response);
      }
      
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '获取日志统计失败');
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
   * 清空日志
   * @returns {Promise<Object>} 操作结果
   */
  async clearLogs() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/logs/clear`, {
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
        const error = new Error(data.error || '清空日志失败');
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

export default LogService; 