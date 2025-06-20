import { ElMessage, ElNotification } from 'element-plus';

/**
 * 消息通知工具类
 */
export class MessageUtil {
  /**
   * 处理 API 错误
   * @param {Error|Object} error 错误对象
   * @param {string} defaultMessage 默认错误消息
   * @param {Object} options 选项配置
   */
  static handleApiError(error, defaultMessage = '操作失败', options = {}) {
    console.error('API Error:', error);
    
    let errorMessage = defaultMessage;
    let errorDetails = null;
    
    // 解析不同类型的错误
    if (error) {
      if (typeof error === 'string') {
        errorMessage = error;
      } else if (error.message) {
        errorMessage = error.message;
      } else if (error.error) {
        errorMessage = error.error;
      } else if (error.data && error.data.error) {
        errorMessage = error.data.error;
      }
      
      // 获取错误详情
      if (error.details) {
        errorDetails = error.details;
      } else if (error.data && error.data.details) {
        errorDetails = error.data.details;
      }
    }
    
    // 根据配置选择显示方式
    if (options.useNotification || errorDetails) {
      ElNotification({
        title: '错误',
        message: errorDetails ? `${errorMessage}\n详情: ${errorDetails}` : errorMessage,
        type: 'error',
        duration: options.duration || 5000,
        showClose: true
      });
    } else {
      ElMessage({
        message: errorMessage,
        type: 'error',
        duration: options.duration || 3000,
        showClose: true
      });
    }
  }

  /**
   * 处理表单验证错误
   * @param {Error} error 错误对象
   * @param {string} customMessage 自定义消息
   */
  static handleValidationError(error, customMessage = '请检查表单填写是否正确') {
    console.error('Validation Error:', error);
    
    let message = customMessage;
    if (error && error.message) {
      message = error.message;
    }
    
    ElMessage({
      message: message,
      type: 'warning',
      duration: 3000,
      showClose: true
    });
  }

  /**
   * 处理网络错误
   * @param {Error} error 错误对象
   */
  static handleNetworkError(error) {
    console.error('Network Error:', error);
    
    let message = '网络连接失败，请检查网络设置';
    
    // 根据不同的网络错误类型提供更具体的信息
    if (error) {
      if (error.code === 'NETWORK_ERROR' || error.message?.includes('fetch')) {
        message = '网络连接失败，请检查网络连接';
      } else if (error.code === 'TIMEOUT_ERROR') {
        message = '请求超时，请稍后重试';
      } else if (error.status) {
        switch (error.status) {
          case 400:
            message = '请求参数错误';
            break;
          case 401:
            message = '未授权访问，请重新登录';
            break;
          case 403:
            message = '访问被拒绝，权限不足';
            break;
          case 404:
            message = '请求的资源不存在';
            break;
          case 500:
            message = '服务器内部错误，请稍后重试';
            break;
          case 502:
            message = '网关错误，请稍后重试';
            break;
          case 503:
            message = '服务暂时不可用，请稍后重试';
            break;
          default:
            message = `网络错误 (${error.status})`;
        }
      }
    }
    
    ElMessage({
      message: message,
      type: 'error',
      duration: 4000,
      showClose: true
    });
  }

  /**
   * 处理成功消息
   * @param {string} message 成功消息
   * @param {Object} options 选项配置
   */
  static handleSuccess(message, options = {}) {
    if (options.useNotification) {
      ElNotification({
        title: '成功',
        message: message,
        type: 'success',
        duration: options.duration || 3000
      });
    } else {
      ElMessage({
        message: message,
        type: 'success',
        duration: options.duration || 2000
      });
    }
  }

  /**
   * 处理警告消息
   * @param {string} message 警告消息
   * @param {Object} options 选项配置
   */
  static handleWarning(message, options = {}) {
    ElMessage({
      message: message,
      type: 'warning',
      duration: options.duration || 3000,
      showClose: true
    });
  }

  /**
   * 处理信息消息
   * @param {string} message 信息消息
   * @param {Object} options 选项配置
   */
  static handleInfo(message, options = {}) {
    if (options.useNotification) {
      ElNotification({
        title: '信息',
        message: message,
        type: 'info',
        duration: options.duration || 3000
      });
    } else {
      ElMessage({
        message: message,
        type: 'info',
        duration: options.duration || 3000,
        showClose: true
      });
    }
  }
} 