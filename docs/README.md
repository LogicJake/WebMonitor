![[docker] CI for releases](https://github.com/LogicJake/WebMonitor/workflows/%5Bdocker%5D%20CI%20for%20releases/badge.svg?branch=master&event=push)
![Tests](https://github.com/LogicJake/WebMonitor/workflows/Tests/badge.svg?branch=master&event=push)
[![telegram](https://img.shields.io/badge/chat-telegram-brightgreen.svg?style=flat-square)](https://t.me/webmonitor_github)

[中文文档](https://www.logicjake.xyz/WebMonitor) | [Telegram 群](https://t.me/webmonitor_github)


## 特性
* 支持requests请求网页，支持使用PhantomJS抓取异步加载的网页
* 支持 xpath 和 css selector 选择器，支持 JsonPath 提取 json 数据
* 支持邮件，pushover 和微信提醒（support by server酱）
* 简洁的UI，可视化操作
* 支持自定义请求头，抓取需要登录的网页
* 支持设置监控规则
* 监控RSS更新

## changelog
### 2019.4.18
***此版本改动较大，旧版本备份在 flask 分支***

* django 下重构，样式更美观
* 仅保留 sqlite 数据库连接方式
* 通知方式可以预先设置无限多，不再限制各种方式各一个

### 2019.3.31
* 修复 RSS 监控无法正常运行 bug
* 添加规则：equal, less, more

### 2019.3.28
* xpath 支持非正式函数 string() 以获取元素及其子元素的所有文本信息

### 2019.3.16
* 支持 JsonPath 提取 json 数据
* 支持 pushover 通知

### 2019.3.13
* 修正规则匹配逻辑
* 修复多种通知方式下, 某一个出错导致的重复发送连锁反应。现在只要用一种方式通知成功, 系统将保存更新后的监控对象, 从而不会在下一次执行时重复发送
* 展现更详细的任务执行状态