## 普通运行
clone 该项目，修改```.env```文件，指定 DATABASE_URL 值为你自己的数据库地址。如果需要使用无头浏览器，请确认已经安装phantomjs，且phantomjs被添加到系统路径。

```
pip install -r requirements.txt
python -m flask run
```