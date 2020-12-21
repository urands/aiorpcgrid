from aiorpcgrid.client import AsyncClient
from aiorpcgrid.protocol.jsonrpc import JsonRPC
from aiorpcgrid.providers.local import LocalProvider
from aiorpcgrid.server import AsyncServer, GlobalAsyncMethods


def register(func=None, name=None):
    if name is not None:
        GlobalAsyncMethods().add(name, func)
    else:
        GlobalAsyncMethods().add(func.__name__, func)


async def create(provider=None, protocol=None, loop=None):
    if protocol is None:
        protocol = JsonRPC()
    if provider is None:
        provider = LocalProvider(protocol)
    return await AsyncServer(provider, loop).create()


async def open(provider=None, protocol=None, loop=None):
    if protocol is None:
        protocol = JsonRPC()
    if provider is None:
        provider = LocalProvider(protocol)
    return await AsyncClient(provider, loop).open()
