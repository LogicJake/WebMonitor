import { ElMessage } from 'element-plus'

/**
 * 处理API响应
 * @param {Promise} promise - API请求Promise
 * @param {Object} options - 配置选项
 * @param {string} options.successMsg - 成功提示消息
 * @param {string} options.errorMsg - 错误提示消息
 * @param {boolean} options.showError - 是否显示错误提示
 * @returns {Promise} 处理后的Promise
 */
export const handleResponse = async (promise, options = {}) => {
  const {
    successMsg = '操作成功',
    errorMsg = '操作失败',
    showError = true
  } = options

  try {
    const response = await promise
    if (response.data.success) {
      if (successMsg) {
        ElMessage.success(successMsg)
      }
      return response.data
    } else {
      throw new Error(response.data.error || errorMsg)
    }
  } catch (error) {
    if (showError) {
      ElMessage.error(error.response?.data?.error || errorMsg)
    }
    throw error
  }
}

/**
 * 创建API响应处理器
 * @param {Object} options - 默认配置选项
 * @returns {Function} 处理函数
 */
export const createResponseHandler = (options = {}) => {
  return (promise, customOptions = {}) => {
    return handleResponse(promise, { ...options, ...customOptions })
  }
} 