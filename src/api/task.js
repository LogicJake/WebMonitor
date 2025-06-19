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
 * 任务相关的 API 服务
 */
export const TaskService = {
  /**
   * 获取所有任务
   * @returns {Promise<Array>} 任务列表
   */
  async getAllTasks() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`);
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 获取单个任务详情
   * @param {number} id 任务ID
   * @returns {Promise<Object>} 任务详情
   */
  async getTaskById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`);
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 创建新任务
   * @param {Object} taskData 任务数据
   * @returns {Promise<Object>} 创建结果
   */
  async createTask(taskData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 更新任务
   * @param {number} id 任务ID
   * @param {Object} taskData 任务数据
   * @returns {Promise<Object>} 更新结果
   */
  async updateTask(id, taskData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 删除任务
   * @param {number} id 任务ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteTask(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 测试任务执行
   * @param {number} id 任务ID
   * @param {boolean} sendNotification 是否发送通知
   * @returns {Promise<Object>} 测试结果
   */
  async testTask(id, sendNotification = false) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          send_notification: sendNotification
        }),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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
   * 测试任务配置（不需要保存任务）
   * @param {Object} taskData 任务配置数据
   * @param {boolean} sendNotification 是否发送通知
   * @returns {Promise<Object>} 测试结果
   */
  async testTaskConfig(taskData, sendNotification = false) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...taskData,
          send_notification: sendNotification
        }),
      });
      if (!response.ok) {
        throw await parseApiError(response);
      }
      return await response.json();
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