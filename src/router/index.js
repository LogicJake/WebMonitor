import { createRouter, createWebHistory } from 'vue-router';
import TaskList from '../components/TaskList.vue';
import NotificationList from '../components/NotificationList.vue';
import TaskForm from '../components/TaskForm.vue';
import MonitorStatus from '../components/MonitorStatus.vue';
import LogViewer from '../components/LogViewer.vue';

const routes = [
  {
    path: '/',
    redirect: '/tasks'
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskList
  },
  {
    path: '/task/new',
    name: 'TaskNew',
    component: TaskForm
  },
  {
    path: '/task/edit/:id',
    name: 'TaskEdit',
    component: TaskForm
  },
  {
    path: '/notifications',
    name: 'NotificationList',
    component: NotificationList
  },
  {
    path: '/monitor',
    name: 'MonitorStatus',
    component: MonitorStatus
  },
  {
    path: '/logs',
    name: 'LogViewer',
    component: LogViewer
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router; 