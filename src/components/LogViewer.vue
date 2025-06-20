<template>
  <div class="log-viewer">
    <el-card class="header-card" :body-style="{ padding: '20px' }">
      <div class="header">
        <h2>监控日志</h2>
        <div class="header-actions">
          <el-button type="primary" @click="refreshLogs" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          <el-button type="danger" @click="handleClearLogs" :loading="clearLoading">
            <el-icon><Delete /></el-icon>
            清空日志
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total || 0 }}</div>
            <div class="stat-label">总日志数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card info">
          <div class="stat-item">
            <div class="stat-value">{{ stats.info || 0 }}</div>
            <div class="stat-label">信息</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card warning">
          <div class="stat-item">
            <div class="stat-value">{{ stats.warning || 0 }}</div>
            <div class="stat-label">警告</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card error">
          <div class="stat-item">
            <div class="stat-value">{{ stats.error || 0 }}</div>
            <div class="stat-label">错误</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 过滤器 -->
    <el-card class="filter-card" :body-style="{ padding: '20px' }">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-select v-model="filters.level" placeholder="选择日志级别" clearable @change="applyFilters">
            <el-option label="全部" value="" />
            <el-option label="信息" value="INFO" />
            <el-option label="警告" value="WARNING" />
            <el-option label="错误" value="ERROR" />
            <el-option label="调试" value="DEBUG" />
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-input-number 
            v-model="filters.limit" 
            :min="10" 
            :max="500" 
            :step="10"
            placeholder="显示条数"
            @change="applyFilters"
          />
        </el-col>
      </el-row>
    </el-card>

    <!-- 日志列表 -->
    <el-card class="log-card" :body-style="{ padding: '0' }">
      <div class="log-container" v-loading="loading">
        <div v-if="logs.length === 0" class="empty-logs">
          <el-empty description="暂无日志数据" />
        </div>
        <div v-else class="log-list">
          <div 
            v-for="(log, index) in logs" 
            :key="index" 
            class="log-item"
            :class="getLogLevelClass(log.level)"
          >
            <div class="log-header">
              <div class="log-level">
                <el-tag :type="getLogLevelTag(log.level)" size="small">
                  {{ log.level }}
                </el-tag>
              </div>
              <div class="log-time">
                {{ formatTime(log.timestamp) }}
              </div>
              <div v-if="log.task_name" class="log-task">
                <el-tag size="small" type="info">{{ log.task_name }}</el-tag>
              </div>
            </div>
            <div class="log-message">
              {{ log.message }}
            </div>
            <div v-if="log.extra && Object.keys(log.extra).length > 0" class="log-extra">
              <el-collapse>
                <el-collapse-item title="详细信息" name="extra">
                  <div class="extra-content">
                    <div v-for="(value, key) in log.extra" :key="key" class="extra-item">
                      <span class="extra-key">{{ key }}:</span>
                      <span class="extra-value">{{ value }}</span>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { ElMessageBox } from 'element-plus';
import { Refresh, Delete } from '@element-plus/icons-vue';
import { LogService } from '@/api/log';
import { MessageUtil } from '@/utils/message-util';

export default {
  name: 'LogViewer',
  
  components: {
    Refresh,
    Delete
  },
  
  setup() {
    const loading = ref(false);
    const clearLoading = ref(false);
    const logs = ref([]);
    const stats = ref({});
    
    const filters = ref({
      level: '',
      limit: 100
    });
    
    const loadLogs = async () => {
      try {
        loading.value = true;
        const data = await LogService.getLogs(filters.value);
        logs.value = data;
      } catch (error) {
        console.error('获取日志失败:', error);
        if (error.code === 'NETWORK_ERROR') {
          MessageUtil.handleNetworkError(error);
        } else {
          MessageUtil.handleApiError(error, '获取日志失败');
        }
      } finally {
        loading.value = false;
      }
    };
    
    const loadStats = async () => {
      try {
        const data = await LogService.getLogStats();
        stats.value = data;
      } catch (error) {
        console.error('获取统计信息失败:', error);
        if (error.code === 'NETWORK_ERROR') {
          MessageUtil.handleNetworkError(error);
        } else {
          MessageUtil.handleApiError(error, '获取统计信息失败');
        }
      }
    };
    
    const refreshLogs = async () => {
      await Promise.all([loadLogs(), loadStats()]);
    };
    
    const applyFilters = () => {
      loadLogs();
    };
    
    const handleClearLogs = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要清空所有日志吗？此操作不可恢复。',
          '确认清空',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        );
        
        clearLoading.value = true;
        await LogService.clearLogs();
        MessageUtil.handleSuccess('日志已清空');
        await refreshLogs();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('清空日志失败:', error);
          if (error.code === 'NETWORK_ERROR') {
            MessageUtil.handleNetworkError(error);
          } else {
            MessageUtil.handleApiError(error, '清空日志失败');
          }
        }
      } finally {
        clearLoading.value = false;
      }
    };
    
    const getLogLevelClass = (level) => {
      return `log-level-${level.toLowerCase()}`;
    };
    
    const getLogLevelTag = (level) => {
      const tagMap = {
        'INFO': 'primary',
        'WARNING': 'warning',
        'ERROR': 'danger',
        'DEBUG': 'info'
      };
      return tagMap[level] || 'default';
    };
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleString('zh-CN');
    };
    
    onMounted(() => {
      refreshLogs();
    });
    
    onUnmounted(() => {
      // 组件卸载时的清理工作
    });
    
    return {
      loading,
      clearLoading,
      logs,
      stats,
      filters,
      refreshLogs,
      applyFilters,
      handleClearLogs,
      getLogLevelClass,
      getLogLevelTag,
      formatTime
    };
  }
};
</script>

<style scoped>
.log-viewer {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.info {
  border-left: 4px solid var(--el-color-primary);
}

.stat-card.warning {
  border-left: 4px solid var(--el-color-warning);
}

.stat-card.error {
  border-left: 4px solid var(--el-color-danger);
}

.stat-item {
  padding: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-text-color-primary);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.filter-card {
  margin-bottom: 20px;
}

.log-card {
  min-height: 400px;
}

.log-container {
  max-height: 600px;
  overflow-y: auto;
}

.empty-logs {
  padding: 40px;
  text-align: center;
}

.log-list {
  padding: 0;
}

.log-item {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  transition: background-color 0.3s;
}

.log-item:hover {
  background-color: var(--el-fill-color-lighter);
}

.log-item:last-child {
  border-bottom: none;
}

.log-level-error {
  border-left: 4px solid var(--el-color-danger);
  background-color: rgba(245, 108, 108, 0.05);
}

.log-level-warning {
  border-left: 4px solid var(--el-color-warning);
  background-color: rgba(230, 162, 60, 0.05);
}

.log-level-info {
  border-left: 4px solid var(--el-color-primary);
  background-color: rgba(64, 158, 255, 0.05);
}

.log-level-debug {
  border-left: 4px solid var(--el-color-info);
  background-color: rgba(144, 147, 153, 0.05);
}

.log-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.log-level {
  flex-shrink: 0;
}

.log-time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  flex-shrink: 0;
}

.log-task {
  flex-shrink: 0;
}

.log-message {
  font-size: 14px;
  color: var(--el-text-color-primary);
  line-height: 1.5;
  word-break: break-all;
  margin-bottom: 8px;
}

.log-extra {
  margin-top: 8px;
}

.extra-content {
  background-color: var(--el-fill-color-lighter);
  padding: 12px;
  border-radius: 4px;
}

.extra-item {
  display: flex;
  margin-bottom: 4px;
  font-size: 12px;
}

.extra-item:last-child {
  margin-bottom: 0;
}

.extra-key {
  font-weight: 500;
  color: var(--el-text-color-regular);
  margin-right: 8px;
  min-width: 80px;
}

.extra-value {
  color: var(--el-text-color-primary);
  word-break: break-all;
}
</style> 