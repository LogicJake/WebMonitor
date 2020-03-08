## 手动部署

### 安装

下载 [WebMonitor](https://github.com/LogicJake/WebMonitor) 的源码

```
git clone https://github.com/LogicJake/WebMonitor.git
cd WebMonitor
```

下载完成后安装依赖

```
pip install -r requirements.txt

```

必须先设置环境变量 DATABASE_URL , 具体方法见"添加配置"。如果需要使用无头浏览器，请确认已经安装 phantomjs ，且 phantomjs 被添加到系统路径。然后在 WebMonitor 文件夹中运行下面的命令就可以启动

```
python -m flask run -h 0.0.0.0 -p 5000
```

### 添加配置
可以通过设置环境变量来配置 WebMonitor。在项目根目录新建 ```.env``` 文件，每行以 ```NAME=VALUE``` 格式添加环境变量，DATABASE_URL 必填，举例如下:
```
DATABASE_URL=mysql+pymysql://username:password@hostname/database
```

## Docker 部署

### 安装

运行下面的命令下载 WebMonitor 镜像

```
docker pull logicjake/webmonitor
```

然后运行 webmonitor 即可

```
docker run -d --name webmonitor -p 5000:5000 -e DATABASE_URL=mysql+pymysql://username:password@hostname/database logicjake/webmonitor
```

您可以使用下面的命令来关闭 webmonitor

```
docker stop webmonitor
```

### 添加配置
在运行时增加参数: -e NAME=VALUE，DATABASE_URL 必须添加
```
-e DATABASE_URL=mysql+pymysql://username:password@hostname/database
```