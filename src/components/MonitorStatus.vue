<template>
  <div class="monitor-status">
    <div class="status-card">
      <div class="status-header">
        <h3>监控服务状态</h3>
        <div class="status-indicator" :class="{ 'running': status.running, 'stopped': !status.running }">
          <span class="indicator-dot"></span>
          {{ status.running ? '运行中' : '已停止' }}
        </div>
      </div>
      
      <div class="status-details" v-if="status">
        <div class="detail-row">
          <span class="label">线程状态:</span>
          <span class="value" :class="{ 'healthy': status.thread_alive, 'error': !status.thread_alive }">
            {{ status.thread_alive ? '正常' : '异常' }}
          </span>
        </div>
        
        <div class="detail-row">
          <span class="label">监控任务数:</span>
          <span class="value">{{ status.monitored_tasks }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">检查次数:</span>
          <span class="value">{{ status.check_count }}</span>
        </div>
        
        <div class="detail-row">
          <span class="label">错误次数:</span>
          <span class="value" :class="{ 'error': status.error_count > 0 }">{{ status.error_count }}</span>
        </div>
        
        <div class="detail-row" v-if="status.last_check_time">
          <span class="label">最后检查:</span>
          <span class="value">{{ formatTime(status.last_check_time) }}</span>
        </div>
      </div>
      
      <div class="status-actions">
        <button 
          class="btn btn-primary" 
          @click="startMonitor" 
          :disabled="status.running || loading"
        >
          启动监控
        </button>
        
        <button 
          class="btn btn-danger" 
          @click="stopMonitor" 
          :disabled="!status.running || loading"
        >
          停止监控
        </button>
        
        <button 
          class="btn btn-secondary" 
          @click="refreshStatus"
          :disabled="loading"
        >
          刷新状态
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { MonitorService } from '@/api/monitor'
import { MessageUtil } from '@/utils/message-util'

export default {
  name: 'MonitorStatus',
  data() {
    return {
      status: {
        running: false,
        thread_alive: false,
        monitored_tasks: 0,
        check_count: 0,
        error_count: 0,
        last_check_time: null
      },
      loading: false,
      refreshTimer: null
    }
  },
  
  mounted() {
    this.refreshStatus()
    // 每30秒自动刷新状态
    this.refreshTimer = setInterval(() => {
      this.refreshStatus()
    }, 30000)
  },
  
  beforeUnmount() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer)
    }
  },
  
  methods: {
    async refreshStatus() {
      try {
        this.loading = true
        const data = await MonitorService.getStatus()
        this.status = data
      } catch (error) {
        console.error('获取监控状态失败:', error)
        if (error.code === 'NETWORK_ERROR') {
          MessageUtil.handleNetworkError(error)
        } else {
          MessageUtil.handleApiError(error, '获取监控状态失败')
        }
      } finally {
        this.loading = false
      }
    },
    
    async startMonitor() {
      try {
        this.loading = true
        const data = await MonitorService.start()
        MessageUtil.handleSuccess(data.message || '监控服务启动成功')
        await this.refreshStatus()
      } catch (error) {
        console.error('启动监控失败:', error)
        if (error.code === 'NETWORK_ERROR') {
          MessageUtil.handleNetworkError(error)
        } else {
          MessageUtil.handleApiError(error, '启动监控失败')
        }
      } finally {
        this.loading = false
      }
    },
    
    async stopMonitor() {
      try {
        this.loading = true
        const data = await MonitorService.stop()
        MessageUtil.handleSuccess(data.message || '监控服务停止成功')
        await this.refreshStatus()
      } catch (error) {
        console.error('停止监控失败:', error)
        if (error.code === 'NETWORK_ERROR') {
          MessageUtil.handleNetworkError(error)
        } else {
          MessageUtil.handleApiError(error, '停止监控失败')
        }
      } finally {
        this.loading = false
      }
    },
    
    formatTime(timeStr) {
      if (!timeStr) return '-'
      const date = new Date(timeStr)
      return date.toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.monitor-status {
  padding: 20px;
}

.status-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e8e8e8;
}

.status-header h3 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.status-indicator.running {
  background: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-indicator.stopped {
  background: #fff2f0;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.status-details {
  margin-bottom: 24px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-weight: 500;
}

.value {
  color: #333;
}

.value.healthy {
  color: #52c41a;
}

.value.error {
  color: #ff4d4f;
}

.status-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1890ff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #40a9ff;
}

.btn-danger {
  background: #ff4d4f;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #ff7875;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover:not(:disabled) {
  background: #e8e8e8;
}
</style> 