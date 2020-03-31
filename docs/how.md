## 登录系统   
首次初始化数据库，系统会自动新建用户，默认用户名为```admin```，默认密码为```admin```，登录之后可以在账号密码管理中修改。进入```/login```，输入账号密码登录。  

登录之后显示如下栏目  

![展示](https://github.com/LogicJake/WebMonitor/raw/master/fig/all.png)

## 设置通知方式
在通知方式管理中默认存在两种通知方式：邮件，pushover 和Server酱的微信提醒。邮件提醒只需要设置接收邮箱，微信提醒需要申请 SCKEY，自行搜索 Server 酱注册，简单免费。pushover 需要填写注册就得到的 User Key。  

![通知方式](https://github.com/LogicJake/WebMonitor/raw/master/fig/noti.png)

### 设置系统邮箱
如果采用邮件提醒，则必须设置系统邮箱设置，该邮箱为提醒邮件的发信人。自行根据需要使用的邮箱查找相关设置，密码一般指授权码。  

![系统邮件设置](https://github.com/LogicJake/WebMonitor/raw/master/fig/mail_setting.png)

## 添加网页监控任务
在网页监控任务管理模块添加新任务  

* 必须选择一种通知方式  
* 默认抓取频率为5分钟，自行根据需要调整，单位分钟，不建议调太快，以防反爬  

![任务管理](https://github.com/LogicJake/WebMonitor/raw/master/fig/task_manage.png)  
![添加任务](https://github.com/LogicJake/WebMonitor/raw/master/fig/task_setting.png)  

### 选择器
提供测试页面```/test```，测试是否能够从页面提取所需信息，方便确认xpath或css selector是否填写正确；在测试页面下，使用无头浏览器获取网页，提取信息错误会展示页面截图。  
元素选择器类型可以选择xpath或css selector，可以借助浏览器F12直接copy两种选择器，需要注意的是，往往浏览器copy得到是元素，而不是文本信息，需要做以下补充：  

#### xpath
* 获取元素文本信息，在浏览器得到的选择器后加```/text()```，如  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/text()```

* 获取元素属性信息，在浏览器得到的选择器后加```/@属性名```，如想获取元素href值  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/@href```

* 获取元素及其子元素的所有文本信息，在浏览器得到的选择器后加```/string()```，如  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/string()```

#### css selector
* 获取元素文本信息，在浏览器得到的选择器后加```::text```，如  
```div#id3 > h3``` => ```div#id3 > h3::text```

* 获取元素属性信息，在浏览器得到的选择器后加```::attr(属性名)```，如想获取元素href值  
```div#id3 > h3``` => ```div#id3 > h3::attr(href)```

#### JsonPath
针对返回 json 数据的接口, 可以使用 JsonPath 提取数据, 具体教程参考 https://goessner.net/articles/JsonPath/

### 是否选择无头浏览器
如果源网页没有异步加载，可以不使用无头浏览器获取网页
```
建议先选择不使用，假如提交时提示获取不到文本信息，再使用无头浏览器尝试
```

### 正则表达式
如果获取到的文本信息有冗余，可以采用正则进一步筛选，如  
```价格：1390```使用正则```([1-9]\d*)```提取到纯数字1390

### 监控规则
默认不填则文本发生变化就发通知  
命令格式：-命令 参数
支持以下命令：
#### -contain
如：文本发生变化且文本内容包含```上架```
```
-contain 上架
```

#### -increase
如：文本发生变化且相较于旧值，数值增长超过```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-increase 3
```

#### -decrease
如：文本发生变化且相较于旧值，数值减少超过```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-decrease 3
```

#### -equal
如：文本发生变化且等于某个值，数值等于```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-equal 3
```

#### -less
如：文本发生变化且小于某个值，数值小于```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-less 3
```

#### -more
如：文本发生变化且大于某个值，数值大于```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-more 3
```

### 自定义请求头
可以自定义请求时的请求头，主要用于设置Cookie，获取需要登录才能查看的页面，格式为字典，如  
```{'Cookie':'自定义cookie值'}```

## 任务状态查看
可以在任务状态栏目下查看所有任务，包括任务状态（run or stop），上次运行时间，上次运行结果，运行结果包括三类：  

* 监测到变化，最新值：{最新值}  
* 成功执行但未监测到变化  
* 出错显示异常信息  

![任务状态](https://github.com/LogicJake/WebMonitor/raw/master/fig/status.png)  
可以通过修改任务状态，暂停或重启任务  

![状态设置](https://github.com/LogicJake/WebMonitor/raw/master/fig/status_setting.png)

## 添加RSS监控任务
可以在RSS监控任务管理模块添加新RSS监控任务  

![RSS](https://github.com/LogicJake/WebMonitor/raw/master/fig/rss.png)  
![RSS设置](https://github.com/LogicJake/WebMonitor/raw/master/fig/rss_setting.png)