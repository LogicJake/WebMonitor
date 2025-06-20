<template>
  <div class="notification-list">
    <el-card class="header-card" :body-style="{ padding: '20px' }">
      <div class="header">
        <h2>通知方式管理</h2>
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增通知方式
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="20" v-loading="loading">
      <el-col v-for="notification in notifications" :key="notification.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="notification-card" :body-style="{ padding: '20px' }">
          <div class="notification-header">
            <h3 class="notification-title">{{ notification.name }}</h3>
          </div>
          <div class="notification-info">
            <p><i class="el-icon-bell"></i> 类型: <el-tag :type="getTypeTag(notification.type)">{{ getTypeLabel(notification.type) }}</el-tag></p>
            <div class="config-info">
              <p><i class="el-icon-setting"></i> 配置:</p>
              <div class="config-details">
                <div v-if="notification.type === 'email'">
                  <p>邮箱: {{ notification.config.email }}</p>
                  <p>SMTP: {{ notification.config.smtp_server }}:{{ notification.config.smtp_port }}</p>
                </div>
                <div v-else-if="notification.type === 'webhook'">
                  <p>URL: {{ notification.config.url }}</p>
                </div>
                <div v-else-if="notification.type === 'dingtalk'">
                  <p>钉钉机器人</p>
                </div>
                <div v-else-if="notification.type === 'wechat'">
                  <p>企业微信机器人</p>
                </div>
              </div>
            </div>
            <p v-if="notification.created_at"><i class="el-icon-time"></i> 创建时间: {{ new Date(notification.created_at).toLocaleString() }}</p>
          </div>
          <div class="notification-actions">
            <el-button size="small" @click="handleEdit(notification)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(notification)">删除</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="isEdit ? '编辑通知方式' : '新增通知方式'"
      v-model="dialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入通知方式名称" />
        </el-form-item>

        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择通知类型" @change="handleTypeChange">
            <el-option
              v-for="item in notificationTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <!-- 邮箱配置 -->
        <template v-if="form.type === 'email'">
          <el-form-item label="接收邮箱地址" prop="config.email">
            <el-input v-model="form.config.email" placeholder="请输入邮箱地址" />
          </el-form-item>
          <el-form-item label="SMTP服务器" prop="config.smtp_server">
            <el-input v-model="form.config.smtp_server" placeholder="请输入SMTP服务器地址" />
          </el-form-item>
          <el-form-item label="SMTP端口" prop="config.smtp_port">
            <el-input-number v-model="form.config.smtp_port" :min="1" :max="65535" />
          </el-form-item>
          <el-form-item label="用户名" prop="config.username">
            <el-input v-model="form.config.username" placeholder="请输入SMTP用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="config.password">
            <el-input v-model="form.config.password" type="password" placeholder="请输入SMTP密码" />
          </el-form-item>
        </template>

        <!-- Webhook配置 -->
        <template v-if="form.type === 'webhook'">
          <el-form-item label="Webhook URL" prop="config.url">
            <el-input v-model="form.config.url" placeholder="请输入Webhook URL" />
          </el-form-item>
          <el-form-item label="请求方法" prop="config.method">
            <el-select v-model="form.config.method" placeholder="请选择请求方法">
              <el-option label="POST" value="POST" />
              <el-option label="GET" value="GET" />
            </el-select>
          </el-form-item>
        </template>

        <!-- 钉钉配置 -->
        <template v-if="form.type === 'dingtalk'">
          <el-form-item label="Webhook URL" prop="config.webhook_url">
            <el-input v-model="form.config.webhook_url" placeholder="请输入钉钉机器人Webhook URL" />
          </el-form-item>
          <el-form-item label="密钥" prop="config.secret">
            <el-input v-model="form.config.secret" placeholder="请输入钉钉机器人密钥（可选）" />
          </el-form-item>
        </template>

        <!-- 企业微信配置 -->
        <template v-if="form.type === 'wechat'">
          <el-form-item label="Webhook URL" prop="config.webhook_url">
            <el-input v-model="form.config.webhook_url" placeholder="请输入企业微信机器人Webhook URL" />
          </el-form-item>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import { NotificationService } from '@/api/notification';
import { MessageUtil } from '@/utils/message-util';

const loading = ref(false);
const notifications = ref([]);
const dialogVisible = ref(false);
const isEdit = ref(false);
const submitting = ref(false);
const formRef = ref(null);

const notificationTypes = [
  { value: 'email', label: '邮箱通知' },
  { value: 'webhook', label: 'Webhook' },
  { value: 'dingtalk', label: '钉钉机器人' },
  { value: 'wechat', label: '企业微信机器人' }
];

const form = reactive({
  id: null,
  name: '',
  type: '',
  config: {}
});

const rules = {
  name: [
    { required: true, message: '请输入通知方式名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择通知类型', trigger: 'change' }
  ],
  'config.email': [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  'config.smtp_server': [
    { required: true, message: '请输入SMTP服务器地址', trigger: 'blur' }
  ],
  'config.smtp_port': [
    { required: true, message: '请输入SMTP端口', trigger: 'blur' }
  ],
  'config.url': [
    { required: true, message: '请输入Webhook URL', trigger: 'blur' },
    { type: 'url', message: '请输入正确的URL地址', trigger: 'blur' }
  ],
  'config.webhook_url': [
    { required: true, message: '请输入Webhook URL', trigger: 'blur' },
    { type: 'url', message: '请输入正确的URL地址', trigger: 'blur' }
  ]
};

const getTypeLabel = (type) => {
  const typeMap = {
    email: '邮箱通知',
    webhook: 'Webhook',
    dingtalk: '钉钉机器人',
    wechat: '企业微信机器人'
  };
  return typeMap[type] || type;
};

const getTypeTag = (type) => {
  const tagMap = {
    email: 'primary',
    webhook: 'success',
    dingtalk: 'warning',
    wechat: 'info'
  };
  return tagMap[type] || 'default';
};

const loadNotifications = async () => {
  try {
    loading.value = true;
    notifications.value = await NotificationService.getAllNotifications();
  } catch (error) {
    if (error.code === 'NETWORK_ERROR') {
      MessageUtil.handleNetworkError(error);
    } else {
      MessageUtil.handleApiError(error, '获取通知方式列表失败');
    }
  } finally {
    loading.value = false;
  }
};

const showAddDialog = () => {
  isEdit.value = false;
  resetForm();
  dialogVisible.value = true;
};

const handleEdit = (notification) => {
  isEdit.value = true;
  form.id = notification.id;
  form.name = notification.name;
  form.type = notification.type;
  form.config = { ...notification.config };
  dialogVisible.value = true;
};

const handleDelete = async (notification) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除通知方式"${notification.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );
    
    await NotificationService.deleteNotification(notification.id);
    MessageUtil.handleSuccess('通知方式删除成功');
    await loadNotifications();
  } catch (error) {
    if (error !== 'cancel') {
      if (error.code === 'NETWORK_ERROR') {
        MessageUtil.handleNetworkError(error);
      } else {
        MessageUtil.handleApiError(error, '删除通知方式失败');
      }
    }
  }
};

const handleTypeChange = () => {
  form.config = {};
  if (form.type === 'webhook') {
    form.config.method = 'POST';
  }
};

const resetForm = () => {
  form.id = null;
  form.name = '';
  form.type = '';
  form.config = {};
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    submitting.value = true;

    const data = {
      name: form.name,
      type: form.type,
      config: form.config
    };

    if (isEdit.value) {
      await NotificationService.updateNotification(form.id, data);
      MessageUtil.handleSuccess('通知方式更新成功');
    } else {
      await NotificationService.createNotification(data);
      MessageUtil.handleSuccess('通知方式创建成功');
    }

    dialogVisible.value = false;
    await loadNotifications();
  } catch (error) {
    if (error.name === 'ValidationError') {
      MessageUtil.handleValidationError(error);
    } else {
      if (error.code === 'NETWORK_ERROR') {
        MessageUtil.handleNetworkError(error);
      } else {
        MessageUtil.handleApiError(error, isEdit.value ? '更新通知方式失败' : '创建通知方式失败');
      }
    }
  } finally {
    submitting.value = false;
  }
};

onMounted(() => {
  loadNotifications();
});
</script>

<style scoped>
.notification-list {
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

.notification-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.notification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.notification-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  flex: 1;
  margin-right: 10px;
  word-break: break-all;
}

.notification-info {
  margin-bottom: 15px;
}

.notification-info p {
  margin: 8px 0;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.config-info {
  margin-top: 10px;
}

.config-details {
  margin-left: 20px;
  padding: 8px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.config-details p {
  margin: 4px 0;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.notification-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style> 