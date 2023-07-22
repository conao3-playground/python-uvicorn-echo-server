# python-uvicorn-echo-server

## Usage

Run HTTP echo server.

```bash
poetry install
poetry run uvicorn uvicorn_echo_server.__main__:app --reload
```

Then, you can send HTTP request to `http://localhost:8000` and get the same response.

```bash
$ curl localhost:8000 -d 'hello'
hello

$ curl localhost:8000 -d 'python uvicorn echo server'
python uvicorn echo server
```

If you send HTTP request without body, you get `no body` response.

```
$ curl localhost:8000
no body
```
