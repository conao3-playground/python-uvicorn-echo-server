from __future__ import annotations

from typing import Awaitable, Callable, TypeAlias
import typing
import logging
import logging.config
import pathlib

import yaml

if typing.TYPE_CHECKING:
    import uvicorn._types

    HTTPEvent: TypeAlias = (
        uvicorn._types.HTTPResponseStartEvent |
        uvicorn._types.HTTPResponseBodyEvent |
        uvicorn._types.HTTPResponseTrailersEvent |
        uvicorn._types.HTTPServerPushEvent |
        uvicorn._types.HTTPDisconnectEvent
    )


with open(pathlib.Path(__file__).parent / 'logging.conf.yml') as f:
    logging.config.dictConfig(yaml.safe_load(f))


logger = logging.getLogger(__name__)


def main() -> None:
    logger.info('try `poetry run uvicorn uvicorn_echo_server.__main__:app --reload`')


async def app(
    scope: uvicorn._types.Scope,
    receive: uvicorn._types.ASGIReceiveCallable,
    send: Callable[[HTTPEvent], Awaitable[None]],
) -> None:
    logger.info(f'scope: {scope}')
    logger.info(f'receive: {receive}')
    logger.info(f'send: {send}')

    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += bytes(message.get('body', b''))
        more_body = bool(message.get('more_body', False))

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', b'text/plain'),
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': body or b'No body',
        'more_body': False,
    })


if __name__ == '__main__':
    main()
