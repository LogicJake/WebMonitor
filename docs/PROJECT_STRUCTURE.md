# 项目结构

```
wm_v2/
├── api/                          # 后端API服务
│   ├── __init__.py              # 数据库初始化
│   ├── app.py                   # Flask应用入口
│   ├── config/                  # 配置文件
│   │   └── config.py           # 应用配置
│   ├── controllers/             # 控制器层
│   │   ├── task_controller.py  # 任务管理API
│   │   ├── notification_controller.py  # 通知管理API
│   │   ├── monitor_controller.py       # 监控状态API
│   │   └── log_controller.py           # 日志查询API
│   ├── models/                  # 数据模型
│   │   ├── task.py             # 任务模型
│   │   ├── selector.py         # 选择器模型
│   │   ├── change_condition.py # 变化条件模型
│   │   └── notification.py     # 通知方式模型
│   ├── services/                # 业务逻辑层
│   │   ├── task_service.py     # 任务服务
│   │   ├── monitor_service.py  # 监控服务
│   │   ├── notification_service.py    # 通知服务
│   │   └── log_service.py              # 日志服务
│   ├── factories/               # 工厂类
│   │   ├── notification_factory.py    # 通知工厂
│   │   ├── selector_factory.py        # 选择器工厂
│   │   └── fetcher_factory.py         # 网页抓取器工厂
│   └── utils/                   # 工具类
│       └── exceptions.py        # 自定义异常
├── src/                         # 前端源码
│   ├── api/                     # API接口
│   │   ├── task.js             # 任务API
│   │   └── notification.js      # 通知API
│   ├── components/              # Vue组件
│   │   ├── TaskForm.vue        # 任务表单
│   │   ├── TaskList.vue        # 任务列表
│   │   └── NotificationForm.vue # 通知表单
│   ├── router/                  # 路由配置
│   │   └── index.js
│   ├── utils/                   # 工具函数
│   │   └── error-handler.js    # 错误处理
│   ├── App.vue                  # 根组件
│   └── main.js                  # 应用入口
├── public/                      # 静态资源
├── docs/                        # 文档目录
├── requirements.txt             # Python依赖
├── package.json                 # Node.js依赖
├── vite.config.js              # Vite配置
├── .gitignore                  # Git忽略文件
├── LICENSE                     # 许可证
└── README.md                   # 项目说明
```

## 核心模块说明

### 后端架构

- **app.py**: Flask应用主入口，配置路由和中间件
- **monitor_service.py**: 核心监控服务，负责网页抓取和变化检测
- **task_service.py**: 任务管理服务，处理CRUD操作
- **notification_service.py**: 通知方式管理服务
- **fetcher_factory.py**: 网页抓取器工厂，统一管理requests和Playwright抓取方式

### 前端架构

- **TaskForm.vue**: 任务配置表单，左右分栏布局
- **TaskList.vue**: 任务列表展示，支持状态切换
- **NotificationForm.vue**: 通知方式配置
- **router/index.js**: 路由配置，单页应用导航

### 数据模型

- **Task**: 监控任务主表
- **Selector**: 元素选择器表
- **ChangeCondition**: 变化判断条件表
- **Notification**: 通知方式表

### 关键特性

1. **模块化设计**: 清晰的分层架构，工厂类独立管理
2. **工厂模式**: 选择器和通知方式的扩展性，支持插件化
3. **服务层封装**: 业务逻辑与控制器分离
4. **双模式抓取**: 支持requests和Playwright两种抓取方式
5. **响应式前端**: Vue 3 + Element Plus
6. **RESTful API**: 标准化的接口设计 