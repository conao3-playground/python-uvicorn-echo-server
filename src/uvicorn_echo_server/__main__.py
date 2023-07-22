def main() -> None:
    print('try `poetry run uvicorn uvicorn_echo_server.__main__:app --reload`')


async def app(scope, receive, send):
    print(scope, receive, send)

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })


if __name__ == '__main__':
    main()
