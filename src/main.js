// main.js
import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // 核心样式
import App from './App.vue';
import router from './router';

const app = createApp(App);
app.use(ElementPlus);
app.use(router); // 确保正确使用 router
app.mount('#app');