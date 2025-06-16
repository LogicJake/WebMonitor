<template>
  <div class="app-container">
    <el-menu
      :default-active="$route.path"
      class="app-menu"
      mode="horizontal"
      router
    >
      <div class="menu-left">
        <el-menu-item index="/tasks">监控任务列表</el-menu-item>
        <el-menu-item index="/notifications">通知方式</el-menu-item>
        <el-menu-item index="/monitor">监控状态</el-menu-item>
        <el-menu-item index="/logs">监控日志</el-menu-item>
      </div>
    </el-menu>
    
    <div class="app-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'App',
  
  setup() {
    const route = useRoute();
    const activeIndex = computed(() => route.path);

    return {
      activeIndex
    };
  }
};
</script>

<style>
.app-container {
  min-height: 100vh;
  background-color: var(--el-color-background);
}

.app-menu {
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
}

.menu-left {
  display: flex;
}

.menu-right {
  display: flex;
}

.app-content {
  padding: 20px;
}

/* 全局主题变量 */
:root {
  --el-color-primary: #409EFF;
  --el-color-success: #67C23A;
  --el-color-warning: #E6A23C;
  --el-color-danger: #F56C6C;
  --el-color-info: #909399;
  --el-color-background: #F5F7FA;
  --el-color-text: #303133;
  --el-color-border: #DCDFE6;
}
</style>