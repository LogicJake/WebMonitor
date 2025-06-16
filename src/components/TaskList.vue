<template>
  <div class="task-list">
    <el-card class="header-card" :body-style="{ padding: '20px' }">
      <div class="header">
        <h2>监控任务列表</h2>
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增任务
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="20" v-loading="loading">
      <el-col v-for="task in tasks" :key="task.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="task-card" :body-style="{ padding: '20px' }">
          <div class="task-header">
            <h3 class="task-title">{{ task.name }}</h3>
            <el-switch
              v-model="task.active"
              @change="handleToggleStatus(task)"
            />
          </div>
          <div class="task-info">
            <p><i class="el-icon-link"></i> 网址: <span class="task-url">{{ task.url }}</span></p>
            <p><i class="el-icon-time"></i> 检查间隔: {{ task.interval }}秒</p>
            <p><i class="el-icon-aim"></i> 元素选择器: {{ task.selectors?.length || 0 }}个</p>
            <div v-if="task.selectors?.length" class="selectors-list">
              <div v-for="selector in task.selectors" :key="selector.id" class="selector-item">
                <span class="selector-name">{{ selector.name }}</span>
                <el-tag size="small" :type="getSelectorTypeTag(selector.type)">
                  {{ getSelectorTypeLabel(selector.type) }}
                </el-tag>
                <el-tag v-if="selector.regex_expression" size="small" type="info">
                  正则
                </el-tag>
              </div>
            </div>
            <p v-if="task.change_conditions?.length"><i class="el-icon-s-check"></i> 变化判断条件: {{ task.change_conditions.length }}个</p>
            <div v-if="task.change_conditions?.length" class="conditions-list">
              <div v-for="condition in task.change_conditions" :key="condition.id" class="condition-item">
                <span class="condition-text">{{ condition.element_name }} {{ getConditionOperatorLabel(condition.operator) }}</span>
                <span v-if="condition.compare_value" class="condition-value">{{ condition.compare_value }}</span>
              </div>
            </div>
            <p><i class="el-icon-bell"></i> 通知方式: {{ task.notifications?.length || 0 }}个</p>
            <div v-if="task.notifications?.length" class="notifications-list">
              <div v-for="notification in task.notifications" :key="notification.id" class="notification-item">
                <span class="notification-name">{{ notification.name }}</span>
                <el-tag size="small" :type="getNotificationTypeTag(notification.type)">
                  {{ getNotificationTypeLabel(notification.type) }}
                </el-tag>
              </div>
            </div>
            <div v-if="task.message" class="task-message">
              <p><i class="el-icon-document"></i> 消息模板: {{ task.message }}</p>
            </div>
            <p v-if="task.last_check"><i class="el-icon-check"></i> 上次检查: {{ new Date(task.last_check).toLocaleString() }}</p>
            
            <!-- 上次检查内容 -->
            <div v-if="task.last_content" class="last-content-section">
              <div class="content-header" @click="toggleContent(task.id)">
                <i class="el-icon-view"></i>
                <span>上次检查内容</span>
                <el-icon class="expand-icon" :class="{ 'expanded': expandedTasks.has(task.id) }">
                  <ArrowDown />
                </el-icon>
              </div>
              <div v-show="expandedTasks.has(task.id)" class="content-body">
                <div v-if="getLastContentData(task.last_content)" class="content-items">
                  <div 
                    v-for="(value, key) in getLastContentData(task.last_content)" 
                    :key="key" 
                    class="content-item"
                  >
                    <div class="content-label">{{ key }}:</div>
                    <div class="content-value">{{ value || '(空值)' }}</div>
                  </div>
                </div>
                <div v-else class="content-error">
                  内容解析失败
                </div>
              </div>
            </div>
          </div>
          <div class="task-actions">
            <el-button size="small" @click="handleEdit(task)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(task)">删除</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, ArrowDown } from '@element-plus/icons-vue';
import { TaskService } from '@/api/task';
import { ErrorHandler } from '@/utils/error-handler';

const router = useRouter();
const loading = ref(false);
const tasks = ref([]);
const expandedTasks = ref(new Set());

const selectorTypes = {
  xpath: { label: 'XPath', type: 'primary' },
  css: { label: 'CSS Selector', type: 'success' },
  jsonpath: { label: 'JSONPath', type: 'warning' }
};

const notificationTypes = {
  email: { label: '邮箱通知', type: 'primary' },
  webhook: { label: 'Webhook', type: 'success' },
  dingtalk: { label: '钉钉机器人', type: 'warning' },
  wechat: { label: '企业微信机器人', type: 'info' }
};

const conditionOperators = {
  contains: '包含',
  not_contains: '不包含',
  greater_than: '大于',
  less_than: '小于',
  increased: '相比前值增加',
  decreased: '相比前值减少'
};

const getSelectorTypeLabel = (type) => {
  return selectorTypes[type]?.label || type;
};

const getSelectorTypeTag = (type) => {
  return selectorTypes[type]?.type || 'info';
};

const getNotificationTypeLabel = (type) => {
  return notificationTypes[type]?.label || type;
};

const getNotificationTypeTag = (type) => {
  return notificationTypes[type]?.type || 'info';
};

const getConditionOperatorLabel = (operator) => {
  return conditionOperators[operator] || operator;
};

const toggleContent = (taskId) => {
  if (expandedTasks.value.has(taskId)) {
    expandedTasks.value.delete(taskId);
  } else {
    expandedTasks.value.add(taskId);
  }
};

const getLastContentData = (lastContent) => {
  try {
    if (!lastContent) return null;
    const parsed = JSON.parse(lastContent);
    return parsed.elements || parsed;
  } catch (error) {
    console.error('解析上次内容失败:', error);
    return null;
  }
};

const loadTasks = async () => {
  try {
    loading.value = true;
    tasks.value = await TaskService.getAllTasks();
  } catch (error) {
    ErrorHandler.handleApiError(error, '获取任务列表失败');
  } finally {
    loading.value = false;
  }
};

const handleAdd = () => {
  router.push('/task/new');
};

const handleEdit = (task) => {
  router.push(`/task/edit/${task.id}`);
};

const handleDelete = async (task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务"${task.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );
    
    await TaskService.deleteTask(task.id);
    ElMessage.success('任务删除成功');
    await loadTasks();
  } catch (error) {
    if (error !== 'cancel') {
      ErrorHandler.handleApiError(error, '删除任务失败');
    }
  }
};

const handleToggleStatus = async (task) => {
  try {
    await TaskService.updateTask(task.id, { active: !task.active });
    ElMessage.success('任务状态更新成功');
    await loadTasks();
  } catch (error) {
    ErrorHandler.handleApiError(error, '切换状态失败');
    task.active = !task.active; // 回滚状态
  }
};

onMounted(() => {
  loadTasks();
});
</script>

<style scoped>
.task-list {
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

.task-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.task-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  flex: 1;
  margin-right: 10px;
  word-break: break-all;
}

.task-info {
  margin-bottom: 15px;
}

.task-info p {
  margin: 8px 0;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.task-url {
  word-break: break-all;
}

.task-message {
  margin-top: 8px;
  padding: 8px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.task-message p {
  margin: 0;
  font-size: 13px;
  color: var(--el-text-color-regular);
  word-break: break-all;
}

.selectors-list {
  margin-top: 10px;
  padding: 5px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.selector-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.selector-item:last-child {
  margin-bottom: 0;
}

.selector-name {
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.notifications-list {
  margin-top: 10px;
  padding: 5px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.notification-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.notification-item:last-child {
  margin-bottom: 0;
}

.notification-name {
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.task-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* 上次检查内容样式 */
.last-content-section {
  margin-top: 12px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 6px;
  overflow: hidden;
}

.content-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background-color: var(--el-fill-color-lighter);
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.content-header:hover {
  background-color: var(--el-fill-color-light);
}

.expand-icon {
  margin-left: auto;
  transition: transform 0.3s;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.content-body {
  padding: 12px;
  background-color: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-lighter);
}

.content-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.content-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 4px;
  border-left: 3px solid var(--el-color-primary);
}

.content-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--el-text-color-regular);
}

.content-value {
  font-size: 13px;
  color: var(--el-text-color-primary);
  word-break: break-all;
  white-space: pre-wrap;
  max-height: 100px;
  overflow-y: auto;
  padding: 4px 8px;
  background-color: var(--el-bg-color);
  border-radius: 3px;
  border: 1px solid var(--el-border-color-lighter);
}

.content-error {
  text-align: center;
  color: var(--el-color-danger);
  font-size: 13px;
  padding: 12px;
}

.conditions-list {
  margin-top: 10px;
  padding: 5px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.condition-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.condition-item:last-child {
  margin-bottom: 0;
}

.condition-text {
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.condition-value {
  font-size: 12px;
  color: var(--el-color-primary);
  background-color: var(--el-fill-color);
  padding: 2px 6px;
  border-radius: 3px;
}
</style>