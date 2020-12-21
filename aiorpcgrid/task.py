import asyncio
from enum import IntEnum, auto
from uuid import uuid4


class State(IntEnum):
    COMPLETED = 0
    CREATED = auto()
    PENDING = auto()
    RUNNING = auto()
    FAILED = auto()
    TIMEOUT = auto()


class AsyncTask:

    _parallel = True

    def create(self, method, *args, **kwargs):
        self.id = str(uuid4())
        self.method = method
        self.params = args
        self.named_params = kwargs
        self.event = asyncio.Event()
        self.status = State.PENDING
        return self

    async def wait(self, timeout=5):
        try:
            await asyncio.wait_for(self.event.wait(), timeout=timeout)
            self.event.clear()
        except (asyncio.CancelledError, asyncio.TimeoutError):
            self.status = State.TIMEOUT
            if self._callback is not None:
                asyncio.ensure_future(self._callback(self))
        return self.result
