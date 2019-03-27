# I Am Watching You
监测网页变化，完成诸如新文章发布，商品价格变动，新动态提醒任务，通过设置xpath或css selector选择器，完成网页关键信息的提取。监测到更新后，发送通知到邮件或者微信。
## 特性
* 除支持常规requests网页请求外，还支持使用PhantomJS抓取异步加载的网页
* 支持xpath和css selector选择器
* 支持邮件和微信提醒（support by server酱）
* 简洁的UI，可视化操作
## 使用方式
clone该项目，修改```.env```文件，指定DATABASE_URL值为你自己的数据库地址
### 运行
```
pip install -r requirements.txt
python -m flask run
```
### 登录系统   
首次初始化数据库，系统会自动新建用户，默认用户名为```admin```，密码随机生成，记录在log/log.txt中，登录之后可以在账号密码管理中修改。进入127.0.0.1/login，输入账号密码登录。  
登录之后显示如下栏目  

![展示](https://github.com/LogicJake/WebMonitor/raw/master/fig/all.png)
### 设置通知方式
在通知方式管理中默认存在两种通知方式：邮件和Server酱的微信提醒。邮件提醒只需要设置接收邮箱，微信提醒需要申请SCKEY，自行搜索Server酱注册，简单免费。  

![通知方式](https://github.com/LogicJake/WebMonitor/raw/master/fig/noti.png)
### 设置系统邮箱
如果采用邮件提醒，则必须设置系统邮箱设置，该邮箱为提醒邮件的发信人。自行根据需要使用的邮箱查找相关设置，密码一般指授权码。  

![系统邮件设置](https://github.com/LogicJake/WebMonitor/raw/master/fig/mail_setting.png)
### 添加任务
在任务管理模块添加新任务  

![任务管理](https://github.com/LogicJake/WebMonitor/raw/master/fig/task_manage.png)  
![添加任务](https://github.com/LogicJake/WebMonitor/raw/master/fig/task_setting.png)
* 必须选择一种通知方式
* 默认抓取频率为5分钟，自行根据需要调整，单位分钟，不建议调太快，以防反爬
#### 选择器
元素选择器类型可以选择xpath或css selector，可以借助浏览器F12直接copy两种选择器，需要注意的是，往往浏览器copy得到是元素，而不是文本信息，需要做以下补充：  
##### xpath
* 获取元素文本信息，在浏览器得到的选择器后加```/text()```，如  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/text()```
* 获取元素属性信息，在浏览器得到的选择器后加```/@属性名```，如想获取元素href值  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/@href```
##### css selector
* 获取元素文本信息，在浏览器得到的选择器后加```/::text```，如  
```div#id3 > h3``` => ```div#id3 > h3/::text```
* 获取元素属性信息，在浏览器得到的选择器后加```/::attr(属性名)```，如想获取元素href值  
```div#id3 > h3``` => ```div#id3 > h3/::attr(href)```
#### 正则进一步提取
如果获取到的文本信息有冗余，可以采用正则进一步筛选，如  
```价格：1390```使用正则```([1-9]\d*)```提取到纯数字1390
#### 是否选择无头浏览器
如果源网页没有异步加载，可以不使用无头浏览器获取网页
```
建议先选择不使用，假如提交时提示获取不到文本信息，再使用无头浏览器尝试
```
#### 监控规则
目前监控规则没有完善，默认不填即可，只要文本发生变化就通知，待日后完善完成更多复杂规则监控，如数字减少或增多

#### 任务状态查看
可以在任务状态栏目下查看所有任务，包括任务状态（run or stop），上次运行时间，上次运行结果，运行结果包括三类：  

* 监测到变化，最新值：{最新值}  
* 成功执行但未监测到变化  
* 出错显示异常信息  

![任务状态](https://github.com/LogicJake/WebMonitor/raw/master/fig/status.png)  
可以通过修改任务状态，暂停或重启任务  

![状态设置](https://github.com/LogicJake/WebMonitor/raw/master/fig/status_setting.png)

### todo
* 添加cookie设置，获取需要登录才能访问的页面
* 单独设一个页面，测试选择器和正则