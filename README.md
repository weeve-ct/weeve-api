# weeve-api
weeve backend service

Server cli:
- Run dev server: `./server_cli.py run -d`
- Reset db: `./server_cli.py db --reset`
- Print routes: `./server_cli.py routes`

Running mysql locally:
- create container: `./mysql.sh build`
- start mysql `./mysql.sh start`
- stop mysql `./mysql.sh stop`
- delete mysql `./mysql.sh delete`

Routes:
- Auth
  - Login
  - Check Token
  - Signup
- Records
- Tags
- Teams
