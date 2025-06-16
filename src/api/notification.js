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
 * 通知方式相关的 API 服务
 */
export const NotificationService = {
  /**
   * 获取所有通知方式
   * @returns {Promise<Array>} 通知方式列表
   */
  async getAllNotifications() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notifications`);
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '获取通知方式列表失败');
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
   * 获取单个通知方式详情
   * @param {number} id 通知方式ID
   * @returns {Promise<Object>} 通知方式详情
   */
  async getNotificationById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notifications/${id}`);
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '获取通知方式详情失败');
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
   * 创建新通知方式
   * @param {Object} notificationData 通知方式数据
   * @returns {Promise<Object>} 创建结果
   */
  async createNotification(notificationData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(notificationData),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '创建通知方式失败');
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
   * 更新通知方式
   * @param {number} id 通知方式ID
   * @param {Object} notificationData 通知方式数据
   * @returns {Promise<Object>} 更新结果
   */
  async updateNotification(id, notificationData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notifications/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(notificationData),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '更新通知方式失败');
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
   * 删除通知方式
   * @param {number} id 通知方式ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteNotification(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notifications/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error || '删除通知方式失败');
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