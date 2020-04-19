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

如果需要使用无头浏览器，请确认已经安装 phantomjs，且 phantomjs 被添加到系统路径

首次运行需要迁移数据库且设置管理账号，假设账号为 admin，密码为 password，运行端口为 8000

```
python manage.py migrate
python manage.py initadmin --username admin --password password
python manage.py runserver 0.0.0.0:8000 --noreload
```

非首次运行，只需指定端口
```
python manage.py runserver 0.0.0.0:8000 --noreload
```

## Docker 部署

### 安装

运行下面的命令下载 WebMonitor 镜像

```
docker pull logicjake/webmonitor
```

然后运行 webmonitor 即可，假设账号为 admin，密码为 password，运行端口为 8000

```
docker run -d --name webmonitor -p 8000:8000 -e PORT=8000 -e USERNAME=admin -e PASSWORD=password logicjake/webmonitor
```

您可以使用下面的命令来关闭 webmonitor

```
docker stop webmonitor
```
