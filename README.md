# **TransmissionBot**
v.2

#### Телеграмм бот созданный на основе библиотек aiogram (версии 3.0.7b) и transmission-rpc, для управления торрент-качалкой Transmission.

Для установки бота необходим **python3** не ниже версии **3.10**, все остальные зависимости есть в файле **requirements.txt**. А так же нужен сам Transsmision с установленным модулем Transmission-web, скачать его можно на
[официальном сайте](https://transmissionbt.com/).

Бот может принимать файлы типа **.torrent** и **magnet-ссылки** от пользователя и ставить файлы на закачку, сортируя перед этим их по нужным папкам.
Так же есть возможность просмотра списка торрентов, перенос торрентов между папками и их удаление.

Порядок установки бота на **Linux-сервер**, на примере **Ubuntu-сервера**:

1. Проверьте версию python3, которая установлена на сервере (она должна быть не ниже 3.10):
```bash
python3 -V
```
2. Установите Git и проверьте его установку (этот и следующий шаг можно пропустить, если вы хотите использовать **wget** и **curl**).
```bash
sudo apt install git
git --version
```
3. Перейдите в домашний каталог, склонируйте этот репозиторий и перейдите в папку проекта:
```bash
cd ~
git clone https://github.com/ChronoDi/TransmissionBot.git
cd TransmissionBot/
```
4. Все настройки для бота должны храниться в файле .env, пример его заполнения есть в файле .env.dict. Создайте файл .env и откройте его с помощью редактора:
```bash
cp .env.dict .env
vi .env
```
Файл .env состоит из:
```bash
#Bot
#Токен бота полученный от https://t.me/BotFather
BOT_TOKEN=423423423:dsajdhasjdkhasjkdhasd
#Список пользователей, которые будут иметь доступ к боту. Узнать свой id можно у https://t.me/getmyid_bot
ADMINS=5432543,445323432,31231312
```
```bash
#Redis
#Параметр указывает, нужно ли использовать в качестве хранилища состояния бота Redis,
#необходимо это для того, чтобы бот запоминал место, на котором остановил диалог с вами,
#даже если сервер отключится.
#Принимает параметры True(использовать Redis), False(Не использовать)
USE_REDIS=False
#Адрес сервера, где установлен Redis
REDIS_HOST=localhost
```
```bash
#transmission
#Ip сервера, где установлен Transmission
TRANSMISSION_IP=192.168.1.4
#Порт сервера.
TRANSMISSION_PORT=9091
#Имя пользователя, указанное в настройках Transmission, если его нет, можно оставить пустым
TRANSMISSION_USER_NAME=
#Пароль указанный в настройках, если не указан нужно оставить пустым.
TRANSMISSION_PASSWORD=
#Папка указаная в настройках Transmission
DOWNLOAD_FOLDER=/download/
#Название папок, которые будут использоваться для cортировки скаченных файлов.
FILM_FOLDER=F
SERIAL_FOLDER=S
ANOTHER_FOLDER=A
```

5. Если будете использовать Redis, то его нужно установить:
```bash
sudo apt install redis
```

6. Убедитесь что вы все еще находитесь в папке с проектом и установите виртуального окружения для python, создайте его для проекта и активируйте:
```bash
sudo apt install python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
```

7. Проверьте установлен ли pip:
```bash
pip3.10 -V
```
Если нет, то установите его:
```bash
sudo apt install python3-pip
```

8. Загрузите все необходимые зависимости в виртуальное окружение и проверьте установку:
```bash
pip install -r requirements.txt
pip list
```
Вывод должен быть таким:

```bash
Package            Version
------------------ --------
aiofiles           23.1.0
aiogram            3.0.0b7
aiohttp            3.8.4
aiosignal          1.3.1
async-timeout      4.0.2
attrs              23.1.0
certifi            2023.5.7
charset-normalizer 3.1.0
environs           9.5.0
frozenlist         1.3.3
idna               3.4
magic-filter       1.0.9
marshmallow        3.19.0
multidict          6.0.4
packaging          23.1
pip                20.3.4
pkg-resources      0.0.0
pydantic           1.10.9
python-dotenv      1.0.0
redis              4.5.5
requests           2.31.0
setuptools         44.1.1
transmission-rpc   4.3.0
typing-extensions  4.6.3
urllib3            2.0.3
yarl               1.9.2
```

Проект установлен, достаточно запустить модуль app.py, но если нужно, чтобы бот сам запускался при запуске сервера, нужно создать файл TransmissionBot.service в systemd. Для этого:

1. Перейдите в папку /etc/systemd/system/ и создайте там файл TransmissionBot.service
```bash
cd /etc/systemd/system/
sudo vi TransmissionBot.service
````

2. Запишите в него следующее:
```textmate
[Unit]
Description=TransmissionBot
After=syslog.target
After=network.target

[Service]
Type=simple
User=<ваше имя пользователя>
WorkingDirectory=/home/<ваше имя пользователя>/TransmissionBot
ExecStart=/home/<ваше имя пользователя>/TransmissionBot/venv/bin/python3.10 /home/<ваше имя пользователя>/TransmissionBot/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Перезапустите systemd и активируйте скрипт:
```bash
sudo systemctl enable TransmissionBot.service
sudo systemctl start TransmissionBot.service
```

4. Если нужно остановить скрипт:
```bash
sudo systemctl stop TransmissionBot.service
```

5. Посмотреть статус сервиса бота:
```bash
sudo systemctl status TransmissionBot.service
```
