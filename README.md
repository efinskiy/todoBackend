# Todo Backend

A simple Todo server, features registration, JWT authorization, receiving tasks, creating tasks, deleting tasks, and modifying tasks.

## Quick start
Clone repository
```shell
git clone https://github.com/efinskiy/todoBackend.git
cd todoBackend
```
Create .env file and edit it
```shell
cp .env-example .env
nano .env
```
Create python venv
```shell
python3 -m venv .venv
```
Activate it
```shell
source .venv/bin/activate
```
Install requirements
```shell
pip3 install -r requirements.txt
```
Migrate database
```shell
alembic upgrade head
```

Run uvicorn server
```shell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Docker
Git clone project 
```shell
git clone https://github.com/efinskiy/todoBackend.git
cd todoBackend
```
Create .env file and edit it
```shell
cp .env-example .env
nano .env
```
Build and run image
```shell
docker build -t todo_backend_image . 
docker run -d --name todo_backend -p 8000:8000 --restart unless-stopped todo_backend_image
```

