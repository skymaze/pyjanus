import asyncio
import json
from typing import Dict
from pyee import AsyncIOEventEmitter

from .handle import Handle
from .utils import wait_for


class Session(AsyncIOEventEmitter):
    def __init__(self, session_id, client, loop, keepalive_timeout=0):
        super().__init__(loop=loop)
        self._loop = loop
        self._session_id = session_id
        self._client = client
        self._handles: Dict[str, Handle] = {}
        self._keepalive_timeout = keepalive_timeout
        if keepalive_timeout:
            self._keepalive_task = self._loop.create_task(self._run_keepalive())
        else:
            self._keepalive_task = None

    async def send(self, payload, ack_only: bool = False, timeout=5):
        payload["session_id"] = self._session_id
        return await self._client.send(payload, ack_only, timeout=timeout)

    async def on_session_message(self, message):
        if message["sender"] is not None:
            handle = self._handles.get(message["sender"])
            await handle.on_handle_data(message)
        else:
            self.emit("message", message)

    async def attach(self, plugin: str):
        transaction = await self.send({"janus": "attach", "plugin": plugin})
        response = await wait_for(transaction.response, 5)
        if response.get("janus") == "success":
            handle_id = response["data"]["id"]
            handle = Handle(handle_id=handle_id, session=self, loop=self._loop)
            self._handles[handle_id] = handle
            return handle

        raise Exception(json.dumps(response))

    async def keepalive(self):
        await self.send({"janus": "keepalive"}, ack_only=True)

    async def _run_keepalive(self):
        while self._keepalive_timeout:
            await asyncio.sleep(self._keepalive_timeout)
            await self.keepalive()

    async def close(self):
        self._keepalive_timeout = 0
        self._keepalive_task.cancel()
        try:
            await self._keepalive_task
        except asyncio.CancelledError:
            pass
