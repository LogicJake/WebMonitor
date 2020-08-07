## Set notification mode 
Supports three notification methods: email, pushover, and WeChat alerts. Email reminder only needs to set up the receiving mailbox, WeChat reminder needs to apply for SCKEY, search the Server 酱 to register, simple and free. The Pushover needs to fill in the User Key to register.

### Set system mailbox
If you use mail reminders, you must set up the system mailbox, which is the sender of the reminder messages. According to the need to to find relevant settings, password generally refers to the authorization code.

System mailbox configuration only needs to be set one, more than one default only takes effect the first.

### Set the Pushover Application
If you use the Pushover alert, you must set the Pushover API Token.

## Add a web monitoring task
Add a new task in 'task management > web monitoring management'

* You must select a form of notification
* The default grab frequency is 5 minutes, adjust it according to the need, unit minutes, it is not recommended to adjust too fast, in order to prevent backcrawling

![任务管理](../fig/task_manage.png)  
![添加任务](../fig/task_setting.png)  

### selector
The element selector type can be Xpath, Css selector or JsonPath, and the first two selectors can be copied directly with the help of the browser F12. It's important to note that the browser often copies the element, rather than the text information. The following should be added:

#### xpath
* Gets the element text information by adding ```/text()``` after the selector obtained by the browser, for example:   
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/text()```

* Gets the element attribute information, adding the ```/@attribute name``` after the selector obtained by the browser, if you want to get the element href value:  
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/@href```

* Gets all the text information for the element and its children, adding ```/string()``` after the selector obtained by the browser, for example:     
```//*[@id="id3"]/h3``` => ```//*[@id="id3"]/h3/string()```

#### css selector
* Gets the element text information by adding ```::text``` after the selector obtained by the browser, for example:   
```div#id3 > h3``` => ```div#id3 > h3::text```

* Gets the element attribute information, adding the ```::attr(href)``` after the selector obtained by the browser, if you want to get the element href value: 
```div#id3 > h3``` => ```div#id3 > h3::attr(href)```

#### JsonPath
To return the json data interface, can use JsonPath extract data, specific reference https://goessner.net/articles/JsonPath/

### Whether to select a headless browser
If the source page is not asynchronously loaded, you can get the page without using a headless browser  
```
It is recommended that you choose not to use it first. If you are not prompted for text information when submitting, then try using a headless browser
```

### 正则表达式
If the obtained text information is redundant, regular filtering can be used for further filtering, such as  
```价格：1390``` Using the regular ```([1-9]\d*)``` to extract the pure number 1390

### Monitoring rules
The default is to send notifications when text changes.  
Command format: - Command parameters. Support the following commands:  

#### -contain
For example, the text changes and the text content contains```上架```
```
-contain 上架
```

#### -increase
For example, the text changes and the value increases more than the old value```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-increase 3
```

#### -decrease
For example, the text changes and the value decreases more than the old value```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-decrease 3
```

#### -equal
For example, the text changes and equals a value, the value equals```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-equal 3
```

#### -less
For example: text changes and is less than a value, the value is less than```3```  
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-less 3
```

#### -more
For example, the text changes and is greater than a certain value, the value is greater than```3```    
```如果文本内容不是纯数字，请用正则提取出纯数字，否则将会报错```
```
-more 3
```

### Customize the request header
The request header at the time of request can be customized, which is mainly used to set cookies and obtain the page that can only be viewed by logging in, in the format of dictionary, such as  
```{'Cookie':'Custom cookie values'}```

## Add RSS monitoring tasks
You can add new RSS monitoring tasks to task management > RSS monitoring task management  

![RSS](../fig/rss.png)    

![RSS设置](../fig/rss_setting.png)

## Task status view
You can view all tasks under the task Status column, including task status (Run or Stop), last run time, last run results, and three types of running results:

* Change detected, latest value: {latest value}
* Successful implementation but no changes were detected
* Error displays an exception message

![任务状态](../fig/status.png)  

You can pause or restart a task by changing its status.

## Data import and export
***WARNING: The notification mode of web monitoring task and RSS monitoring task is connected with the notification mode table through foreign keys. In case of changes in the data table, the foreign key ID may be invalid or cannot be consistent with that of export. It is recommended to check whether the notification mode is normal after importing the task data. ***