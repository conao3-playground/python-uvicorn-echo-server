import logging
import logging.config
import pathlib

import yaml


with open(pathlib.Path(__file__).parent / 'logging.conf.yml') as f:
    logging.config.dictConfig(yaml.safe_load(f))


logger = logging.getLogger(__name__)


def main() -> None:
    logger.info('try `poetry run uvicorn uvicorn_echo_server.__main__:app --reload`')


async def app(scope, receive, send):
    logger.info(f'scope: {scope}')
    logger.info(f'receive: {receive}')
    logger.info(f'send: {send}')

    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': body or b'No body',
    })


if __name__ == '__main__':
    main()
