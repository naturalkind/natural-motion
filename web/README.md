### Тестовая сборка для работы в браузере    
1. установка
```
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements3.6.txt
```
> [!CAUTION]
> `sudo chmod 777 /nn/Lifting-from-the-Deep-release-master/setup.sh`
> `./nn/Lifting-from-the-Deep-release-master/setup.sh` - скачать веса и установить необходимые lib

2.  запуск <a href="https://docs.celeryq.dev/en/stable/">celery</a>   
```
celery -A start_celery worker --loglevel=info
```
3. запуск простого сервера tornado
```
python3 server.py
```

