<template>
  <div class="task-form">
    <div class="form-layout">
      <!-- 左侧表单区域 -->
      <div class="form-section">
        <el-card class="form-card">
          <template #header>
            <div class="card-header">
              <span>{{ isEdit ? '编辑任务' : '新增任务' }}</span>
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="100px"
            @submit.prevent
          >
        <el-form-item label="任务名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入任务名称"
            :maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="监控网址" prop="url">
          <el-input
            v-model="form.url"
            placeholder="请输入要监控的网页URL"
            type="url"
          />
        </el-form-item>

        <el-form-item label="抓取方式" prop="use_playwright">
          <el-select v-model="form.use_playwright" placeholder="请选择抓取方式" style="width: 100%">
            <el-option
              :value="false"
              label="requests（快速）"
            >
              <div>
                <div>requests（快速）</div>
                <div class="option-description">适用于静态网页，速度快，资源占用少</div>
              </div>
            </el-option>
            <el-option
              :value="true"
              label="Playwright（浏览器）"
            >
              <div>
                <div>Playwright（浏览器）</div>
                <div class="option-description">适用于需要JavaScript渲染的动态网页，支持SPA应用</div>
              </div>
            </el-option>
          </el-select>
          <div class="form-item-tip">
            💡 提示：requests模式适合大部分静态网页，响应速度快；Playwright模式适合需要JavaScript渲染的动态网页（如SPA应用），但会消耗更多资源。
          </div>
        </el-form-item>

        <el-form-item label="监控间隔" prop="interval">
          <el-input-number
            v-model="form.interval"
            :min="1"
            :max="3600"
            :step="1"
          />
          <span class="unit">秒</span>
        </el-form-item>

        <el-form-item label="自定义请求头" prop="custom_headers">
          <el-input
            v-model="form.custom_headers"
            type="textarea"
            :rows="4"
            placeholder='请输入自定义请求头，格式为JSON。例如：{"Authorization": "Bearer token123", "Accept": "application/json"}'
            :maxlength="2000"
            show-word-limit
          />
          <div class="form-item-tip">
            💡 提示：自定义请求头为可选项，用于在HTTP请求中添加额外的头部信息。格式必须为有效的JSON对象，如：<code>{"key": "value"}</code>
          </div>
        </el-form-item>

        <el-form-item label="通知方式" prop="notification_ids">
          <el-select
            v-model="form.notification_ids"
            multiple
            placeholder="请选择通知方式"
            style="width: 100%"
            :loading="notificationsLoading"
          >
            <el-option
              v-for="notification in notifications"
              :key="notification.id"
              :label="notification.name"
              :value="notification.id"
            >
              <span>{{ notification.name }}</span>
              <el-tag size="small" :type="getNotificationTypeTag(notification.type)" style="margin-left: 8px">
                {{ getNotificationTypeLabel(notification.type) }}
              </el-tag>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="元素选择器" prop="selectors">
          <div class="selectors-container">
            <div v-for="(selector, index) in form.selectors" :key="index" class="selector-item">
              <el-row :gutter="10">
                <el-col :span="5">
                  <el-input
                    v-model="selector.name"
                    placeholder="元素名称"
                    maxlength="100"
                    show-word-limit
                  />
                </el-col>
                <el-col :span="4">
                  <el-select v-model="selector.type" placeholder="选择器类型">
                    <el-option
                      v-for="item in selectorTypes"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="7">
                  <el-input
                    v-model="selector.expression"
                    placeholder="选择器表达式"
                    maxlength="500"
                    show-word-limit
                  />
                </el-col>
                <el-col :span="6">
                  <el-input
                    v-model="selector.regex_expression"
                    placeholder="正则表达式（可选）"
                    maxlength="500"
                    show-word-limit
                  />
                </el-col>
                <el-col :span="2">
                  <el-button
                    type="danger"
                    :icon="Delete"
                    circle
                    @click="removeSelector(index)"
                    :disabled="form.selectors.length <= 1"
                  />
                </el-col>
              </el-row>
            </div>
            <el-button
              type="primary"
              icon="Plus"
              @click="addSelector"
              class="add-selector-btn"
            >
              添加选择器
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="消息模板" prop="message">
          <el-input
            v-model="form.message"
            type="textarea"
            :rows="4"
            placeholder="请输入消息模板，支持使用{元素名称}进行变量替换。例如：价格变化了，当前价格为{price}。如不填写将使用默认模板。"
            :maxlength="5000"
            show-word-limit
          />
          <div class="form-item-tip">
            💡 提示：可以使用 <code>{元素名称}</code> 的格式在消息中引用选择器提取的值。如不填写消息模板，系统将自动使用"元素名:值"的格式，用制表符连接所有元素。
          </div>
        </el-form-item>

        <el-form-item label="变化判断条件" prop="change_conditions">
          <div class="conditions-container">
            <div v-for="(condition, index) in form.change_conditions" :key="index" class="condition-item">
              <el-row :gutter="10">
                <el-col :span="5">
                  <el-select v-model="condition.element_name" placeholder="选择元素">
                    <el-option
                      v-for="selector in form.selectors"
                      :key="selector.name"
                      :label="selector.name"
                      :value="selector.name"
                    />
                  </el-select>
                </el-col>
                <el-col :span="5">
                  <el-select v-model="condition.operator" placeholder="判断条件">
                    <el-option
                      v-for="op in operatorTypes"
                      :key="op.value"
                      :label="op.label"
                      :value="op.value"
                    />
                  </el-select>
                </el-col>
                <el-col :span="10">
                  <el-input
                    v-model="condition.compare_value"
                    placeholder="比较值"
                    maxlength="100"
                  />
                </el-col>
                <el-col :span="4">
                  <el-button
                    type="danger"
                    :icon="Delete"
                    circle
                    @click="removeCondition(index)"
                  />
                  <el-button
                    type="primary"
                    :icon="ArrowUp"
                    circle
                    v-if="index > 0"
                    @click="moveConditionUp(index)"
                  />
                </el-col>
              </el-row>
            </div>
            <el-button
              type="primary"
              icon="Plus"
              @click="addCondition"
              class="add-condition-btn"
            >
              添加判断条件
            </el-button>
            <div class="form-item-tip">
              💡 提示：变化判断条件是可选的。如不添加，将默认判断消息模板内容是否变化。如添加多个条件，按顺序判断，有一个符合即触发通知。<br/>
              • <strong>包含/不包含</strong>：检查元素值是否包含指定文本<br/>
              • <strong>大于/小于</strong>：将元素值作为数字与指定值比较<br/>
              • <strong>相比前值增加/减少</strong>：与上次的值比较，可指定变化幅度（如填写10表示增加/减少10以上才触发）
            </div>
          </div>
        </el-form-item>

        <el-form-item label="状态" prop="active">
          <el-switch
            v-model="form.active"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>

        <!-- 上次检查内容 -->
        <el-form-item v-if="isEdit && taskData && taskData.last_content" label="上次检查内容">
          <div class="last-content-display">
            <el-collapse v-model="activeCollapse">
              <el-collapse-item title="查看上次检查获取的内容" name="content">
                <div v-if="getLastContentData(taskData.last_content)" class="content-items">
                  <div 
                    v-for="(value, key) in getLastContentData(taskData.last_content)" 
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
                <div v-if="taskData.last_check" class="last-check-time">
                  检查时间: {{ new Date(taskData.last_check).toLocaleString() }}
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-form-item>

                    <el-form-item>
              <el-button type="primary" @click="handleSubmit" :loading="submitting">
                {{ isEdit ? '保存' : '创建' }}
              </el-button>
              <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>

      <!-- 右侧测试区域 -->
      <div class="test-section">
        <el-card class="test-card">
          <template #header>
            <div class="card-header">
              <span>任务测试</span>
            </div>
          </template>

          <div class="test-content">
            <div class="test-actions">
              <el-button 
                type="success" 
                @click="handleTest" 
                :loading="testing"
                size="large"
                style="width: 100%;"
              >
                <el-icon><PlayIcon /></el-icon>
                测试任务
              </el-button>
              <div class="test-options">
                <el-checkbox v-model="testSendNotification" style="margin-top: 10px;">
                  测试时发送通知（仅在检测到变化时发送）
                </el-checkbox>
              </div>
              <div class="test-description">
                <el-text type="info" size="small">
                  点击测试按钮验证任务配置是否正确，包括网页抓取、元素提取、消息模板等功能。
                </el-text>
              </div>
            </div>

            <!-- 测试结果显示 -->
            <div v-if="testResult" class="test-result-container">
              <el-alert
                :title="testResult.success ? '测试成功' : '测试失败'"
                :type="testResult.success ? 'success' : 'error'"
                :closable="false"
                show-icon
              />
              
              <div v-if="testResult.success" class="test-details">
                <el-descriptions title="执行详情" :column="1" border>
                  <el-descriptions-item label="响应时间">
                    {{ testResult.response_time ? testResult.response_time.toFixed(3) + 's' : 'N/A' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="是否有变化">
                    <el-tag :type="testResult.has_changed ? 'warning' : 'info'">
                      {{ testResult.has_changed ? '有变化' : '无变化' }}
                    </el-tag>
                  </el-descriptions-item>
                  <el-descriptions-item label="通知发送">
                    <el-tag :type="testResult.notification_sent ? 'success' : 'info'">
                      {{ testResult.notification_sent ? '已发送' : '未发送' }}
                    </el-tag>
                  </el-descriptions-item>
                </el-descriptions>

                <!-- 提取的元素值 -->
                <div v-if="testResult.elements" class="test-elements">
                  <h4>提取的元素值：</h4>
                  <div class="elements-list">
                    <div 
                      v-for="(value, key) in testResult.elements" 
                      :key="key" 
                      class="element-item"
                    >
                      <div class="element-label">{{ key }}:</div>
                      <div class="element-value">{{ value || '(空值)' }}</div>
                    </div>
                  </div>
                </div>

                <!-- 格式化的消息 -->
                <div v-if="testResult.formatted_message" class="test-message">
                  <h4>格式化消息：</h4>
                  <div class="message-content">
                    {{ testResult.formatted_message }}
                  </div>
                </div>

                <!-- 页面截图 -->
                <div v-if="testResult.screenshot && form.use_playwright" class="test-screenshot">
                  <h4>页面截图：</h4>
                  <div class="screenshot-container">
                    <el-image
                      :src="`data:image/png;base64,${testResult.screenshot}`"
                      :preview-src-list="[`data:image/png;base64,${testResult.screenshot}`]"
                      fit="contain"
                      class="screenshot-image"
                      preview-teleported
                    >
                      <template #error>
                        <div class="image-error">
                          <el-icon><Picture /></el-icon>
                          <span>截图加载失败</span>
                        </div>
                      </template>
                    </el-image>
                    <div class="screenshot-tip">
                      💡 点击图片可放大查看，使用Playwright模式抓取的页面截图
                    </div>
                  </div>
                </div>

                <!-- 通知错误 -->
                <div v-if="testResult.notification_error" class="notification-error">
                  <el-alert
                    title="通知发送失败"
                    :description="testResult.notification_error"
                    type="error"
                    show-icon
                    :closable="false"
                  />
                </div>
              </div>

              <div v-else class="test-error">
                <p><strong>错误信息：</strong>{{ testResult.error }}</p>
                <p v-if="testResult.response_time"><strong>响应时间：</strong>{{ testResult.response_time.toFixed(3) }}s</p>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Delete, ArrowUp, VideoPlay as PlayIcon, Picture } from '@element-plus/icons-vue';
import { TaskService } from '@/api/task';
import { NotificationService } from '@/api/notification';
import { ErrorHandler } from '@/utils/error-handler';

export default {
  name: 'TaskForm',

  setup() {
    const route = useRoute();
    const router = useRouter();
    const formRef = ref(null);
    const isEdit = ref(false);
    const submitting = ref(false);
    const testing = ref(false);
    const testSendNotification = ref(false);
    const notificationsLoading = ref(false);
    const notifications = ref([]);
    const taskData = ref(null);
    const activeCollapse = ref([]);
    const testResult = ref(null);

    const selectorTypes = [
      { value: 'xpath', label: 'XPath' },
      { value: 'css', label: 'CSS Selector' },
      { value: 'jsonpath', label: 'JSONPath' }
    ];

    const operatorTypes = [
      { value: 'contains', label: '包含' },
      { value: 'not_contains', label: '不包含' },
      { value: 'greater_than', label: '大于' },
      { value: 'less_than', label: '小于' },
      { value: 'increased', label: '相比前值增加' },
      { value: 'decreased', label: '相比前值减少' }
    ];

    const form = reactive({
      name: '',
      url: '',
      interval: 60,
      active: true,
      message: '',
      custom_headers: '',
      use_playwright: null,
      selectors: [],
      notification_ids: [],
      change_conditions: []
    });

    const rules = {
      name: [
        { required: true, message: '请输入任务名称', trigger: 'blur' },
        { max: 100, message: '任务名称不能超过100个字符', trigger: 'blur' }
      ],
      url: [
        { required: true, message: '请输入监控网址', trigger: 'blur' },
        { type: 'url', message: '请输入正确的URL地址', trigger: 'blur' }
      ],
      interval: [
        { required: true, message: '请输入检查间隔', trigger: 'blur' },
        { type: 'number', min: 1, max: 3600, message: '检查间隔必须在1-3600秒之间', trigger: 'blur' }
      ],
      message: [
        { max: 5000, message: '消息模板内容不能超过5000个字符', trigger: 'blur' }
      ],
      custom_headers: [
        { max: 2000, message: '自定义请求头不能超过2000个字符', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (!value || value.trim() === '') {
              callback(); // 空值是允许的
              return;
            }
            try {
              const parsed = JSON.parse(value);
              if (typeof parsed !== 'object' || Array.isArray(parsed)) {
                callback(new Error('自定义请求头必须是有效的JSON对象'));
                return;
              }
              callback();
            } catch (error) {
              callback(new Error('自定义请求头格式不正确，请输入有效的JSON'));
            }
          },
          trigger: 'blur'
        }
      ],
      use_playwright: [
        { required: true, message: '请选择抓取方式', trigger: 'change' }
      ],
      notification_ids: [
        { 
          type: 'array',
          required: true,
          message: '至少需要选择一个通知方式',
          trigger: 'change'
        }
      ],
      selectors: [
        { 
          type: 'array',
          required: true,
          message: '至少需要添加一个元素选择器',
          trigger: 'change'
        },
        {
          validator: (rule, value, callback) => {
            if (!value || value.length === 0) {
              callback(new Error('至少需要添加一个元素选择器'));
              return;
            }
            for (const selector of value) {
              if (!selector.name || !selector.type || !selector.expression) {
                callback(new Error('请完整填写所有选择器信息'));
                return;
              }
            }
            callback();
          },
          trigger: 'change'
        }
      ]
    };

    const getNotificationTypeLabel = (type) => {
      const typeMap = {
        email: '邮箱通知',
        webhook: 'Webhook',
        dingtalk: '钉钉机器人',
        wechat: '企业微信机器人'
      };
      return typeMap[type] || type;
    };

    const getNotificationTypeTag = (type) => {
      const tagMap = {
        email: 'primary',
        webhook: 'success',
        dingtalk: 'warning',
        wechat: 'info'
      };
      return tagMap[type] || 'default';
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

    const loadNotifications = async () => {
      try {
        notificationsLoading.value = true;
        notifications.value = await NotificationService.getAllNotifications();
      } catch (error) {
        ErrorHandler.handleApiError(error, '获取通知方式列表失败');
      } finally {
        notificationsLoading.value = false;
      }
    };

    const addSelector = () => {
      form.selectors.push({
        name: '',
        type: 'xpath',
        expression: '',
        regex_expression: ''
      });
    };

    const removeSelector = (index) => {
      form.selectors.splice(index, 1);
    };

    const loadTask = async (id) => {
      try {
        const task = await TaskService.getTaskById(id);
        taskData.value = task; // 保存完整的任务数据
        form.name = task.name;
        form.url = task.url;
        form.interval = task.interval;
        form.active = task.active;
        form.message = task.message || '';
        form.custom_headers = task.custom_headers || '';
        form.use_playwright = task.use_playwright !== undefined ? task.use_playwright : null;
        form.selectors = task.selectors || [];
        form.notification_ids = task.notifications ? task.notifications.map(n => n.id) : [];
        form.change_conditions = task.change_conditions || [];
      } catch (error) {
        ErrorHandler.handleApiError(error, '获取任务信息失败');
      }
    };

    const handleSubmit = async () => {
      if (!formRef.value) return;
      
      try {
        await formRef.value.validate();
        submitting.value = true;

        const data = {
          name: form.name,
          url: form.url,
          interval: form.interval,
          active: form.active,
          message: form.message,
          custom_headers: form.custom_headers,
          use_playwright: form.use_playwright,
          selectors: form.selectors,
          notification_ids: form.notification_ids,
          change_conditions: form.change_conditions
        };

        if (isEdit.value) {
          await TaskService.updateTask(route.params.id, data);
          ElMessage.success('任务更新成功');
        } else {
          await TaskService.createTask(data);
          ElMessage.success('任务创建成功');
        }

        router.push('/tasks');
      } catch (error) {
        if (error.name === 'ValidationError') {
          ElMessage.error('请检查表单填写是否正确');
        } else {
          ErrorHandler.handleApiError(error, isEdit.value ? '更新任务失败' : '创建任务失败');
        }
      } finally {
        submitting.value = false;
      }
    };

    const handleCancel = () => {
      router.push('/tasks');
    };

    const handleTest = async () => {
      try {
        // 先验证表单
        if (!formRef.value) return;
        await formRef.value.validate();
        
        testing.value = true;
        testResult.value = null;

        ElMessage.info('正在执行任务测试...');
        
        // 统一使用任务配置参数进行测试
        const taskData = {
          name: form.name,
          url: form.url,
          interval: form.interval,
          active: form.active,
          message: form.message,
          custom_headers: form.custom_headers,
          use_playwright: form.use_playwright,
          selectors: form.selectors,
          notification_ids: form.notification_ids,
          change_conditions: form.change_conditions,
          send_notification: testSendNotification.value
        };
        
        const result = await TaskService.testTaskConfig(taskData);
        
        testResult.value = result;
        
        if (result.success) {
          ElMessage.success('任务测试完成');
        } else {
          ElMessage.error('任务测试失败');
        }
        
      } catch (error) {
        if (error.name === 'ValidationError') {
          ElMessage.error('请先完整填写任务配置');
          return;
        }
        
        testResult.value = {
          success: false,
          error: error.message || '测试请求失败'
        };
        ErrorHandler.handleApiError(error, '任务测试失败');
      } finally {
        testing.value = false;
      }
    };

    const addCondition = () => {
      form.change_conditions.push({
        element_name: '',
        operator: '',
        compare_value: ''
      });
    };

    const removeCondition = (index) => {
      form.change_conditions.splice(index, 1);
    };

    const moveConditionUp = (index) => {
      if (index > 0) {
        const temp = form.change_conditions[index - 1];
        form.change_conditions[index - 1] = form.change_conditions[index];
        form.change_conditions[index] = temp;
      }
    };

    onMounted(async () => {
      await loadNotifications();
      
      const id = route.params.id;
      if (id) {
        isEdit.value = true;
        await loadTask(id);
      }
    });

    return {
      formRef,
      form,
      rules,
      submitting,
      testing,
      testSendNotification,
      isEdit,
      selectorTypes,
      operatorTypes,
      addSelector,
      removeSelector,
      handleSubmit,
      handleCancel,
      handleTest,
      notificationsLoading,
      notifications,
      getNotificationTypeLabel,
      getNotificationTypeTag,
      taskData,
      activeCollapse,
      getLastContentData,
      addCondition,
      removeCondition,
      moveConditionUp,
      testResult,
      Delete,
      ArrowUp,
      PlayIcon,
      Picture
    };
  }
};
</script>

<style scoped>
.task-form {
  padding: 20px;
}

.form-layout {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.form-section {
  flex: 1;
  min-width: 0;
}

.test-section {
  width: 400px;
  flex-shrink: 0;
}

.form-card,
.test-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.test-card {
  position: sticky;
  top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.unit {
  margin-left: 10px;
  color: var(--el-text-color-secondary);
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-dialog__body) {
  padding-top: 20px;
}

.selectors-container {
  width: 100%;
}

.selector-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
}

.add-selector-btn {
  margin-top: 10px;
  width: 100%;
}

.form-item-tip {
  margin-top: 6px;
  padding: 8px 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  font-size: 13px;
  color: var(--el-text-color-regular);
  line-height: 1.4;
}

.form-item-tip code {
  padding: 2px 4px;
  background-color: var(--el-fill-color);
  border-radius: 2px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  color: var(--el-color-primary);
}

/* 上次检查内容样式 */
.last-content-display {
  width: 100%;
}

.content-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.content-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 6px;
  border-left: 4px solid var(--el-color-primary);
}

.content-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-regular);
}

.content-value {
  font-size: 14px;
  color: var(--el-text-color-primary);
  word-break: break-all;
  white-space: pre-wrap;
  max-height: 120px;
  overflow-y: auto;
  padding: 8px 12px;
  background-color: var(--el-bg-color);
  border-radius: 4px;
  border: 1px solid var(--el-border-color-lighter);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.content-error {
  text-align: center;
  color: var(--el-color-danger);
  font-size: 14px;
  padding: 20px;
}

.last-check-time {
  margin-top: 12px;
  padding: 8px 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  text-align: center;
}

.conditions-container {
  width: 100%;
}

.condition-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
}

.add-condition-btn {
  margin-top: 10px;
  width: 100%;
}

/* 测试区域样式 */
.test-content {
  padding: 0;
}

.test-actions {
  margin-bottom: 20px;
}

.test-options {
  padding: 8px 0;
  border-top: 1px solid var(--el-border-color-lighter);
  border-bottom: 1px solid var(--el-border-color-lighter);
  margin: 10px 0;
}

.test-description {
  margin-top: 10px;
  padding: 8px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  text-align: center;
}

/* 测试结果样式 */
.test-result-container {
  width: 100%;
  margin-top: 20px;
}

.test-details {
  margin-top: 15px;
}

.test-elements {
  margin-top: 20px;
}

.test-elements h4 {
  margin: 0 0 10px 0;
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.elements-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.element-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 6px;
  border-left: 4px solid var(--el-color-success);
}

.element-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--el-text-color-regular);
}

.element-value {
  font-size: 13px;
  color: var(--el-text-color-primary);
  word-break: break-all;
  white-space: pre-wrap;
  max-height: 100px;
  overflow-y: auto;
  padding: 6px 8px;
  background-color: var(--el-bg-color);
  border-radius: 3px;
  border: 1px solid var(--el-border-color-lighter);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.test-message {
  margin-top: 20px;
}

.test-message h4 {
  margin: 0 0 10px 0;
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.message-content {
  padding: 12px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 6px;
  border-left: 4px solid var(--el-color-warning);
  font-size: 13px;
  color: var(--el-text-color-primary);
  word-break: break-all;
  white-space: pre-wrap;
  max-height: 150px;
  overflow-y: auto;
  line-height: 1.5;
}

.test-error {
  margin-top: 15px;
  padding: 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 6px;
  border-left: 4px solid var(--el-color-danger);
}

.test-error p {
  margin: 8px 0;
  font-size: 13px;
  line-height: 1.4;
}

.notification-error {
  margin-top: 15px;
}

/* 截图样式 */
.test-screenshot {
  margin-top: 20px;
}

.test-screenshot h4 {
  margin: 0 0 10px 0;
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.screenshot-container {
  padding: 12px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 6px;
  border-left: 4px solid var(--el-color-primary);
}

.screenshot-image {
  width: 100%;
  max-height: 300px;
  border-radius: 4px;
  border: 1px solid var(--el-border-color-light);
  cursor: pointer;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 150px;
  color: var(--el-text-color-secondary);
  background-color: var(--el-fill-color-light);
}

.image-error .el-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.screenshot-tip {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  text-align: center;
  line-height: 1.4;
}

/* 下拉框选项样式 */
.option-description {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 2px;
  line-height: 1.3;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .form-layout {
    flex-direction: column;
  }
  
  .test-section {
    width: 100%;
  }
  
  .test-card {
    position: static;
  }
}
</style>