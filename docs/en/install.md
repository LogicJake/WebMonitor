## Manual deployment

### Installation

Download the code of [WebMonitor](https://github.com/LogicJake/WebMonitor).

```
git clone https://github.com/LogicJake/WebMonitor.git
cd WebMonitor
```

Install dependencies after download is complete.

```
pip install -r requirements.txt
```

If you need to use a headless browser, make sure 'phantomjs' is installed and added to the system path.

For the first run, the database should be migrated and the admin account should be set, assuming the account is 'admin', password is 'password' and the port is '8000'.

```
python manage.py migrate
python manage.py initadmin --username admin --password password
python manage.py runserver 0.0.0.0:8000 --noreload
```

Not the first run, just specify the port.

```
python manage.py runserver 0.0.0.0:8000 --noreload
```

## Docker deployment

### Installation

Run the following command to download the WebMonitor image.

```
docker pull logicjake/webmonitor
```

Then run WebMonitor, assuming the account is 'admin', password is 'password', and the port is '8000'.  
***It is strongly recommended to save the database file to the host machine through the docker folder mapping parameter -v, otherwise the database file will be lost after container reconstruction, assuming the mapped directory is /etc/webmonitor.***

```
docker run -d --name webmonitor -v /etc/webmonitor:/app/db -p 8000:8000 -e PORT=8000 -e USERNAME=admin -e PASSWORD=password logicjake/webmonitor
```

You can use the following command to turn off WebMonitor.

```
docker stop webmonitor
```
