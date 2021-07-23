import sys
import json
import asyncio
from typing import Dict, Optional
import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
from pyee import AsyncIOEventEmitter

from .utils import get_random_id, wait_for
from .session import Session
from .transaction import Transaction


class Client(AsyncIOEventEmitter):
    def __init__(self, uri: str, loop=None):
        if not loop:
            if sys.version_info.major == 3 and sys.version_info.minor == 6:
                loop = asyncio.get_event_loop()
            else:
                loop = asyncio.get_running_loop()
        super().__init__(loop=loop)
        self._uri = uri
        self._websocket: Optional[WebSocketCommonProtocol] = None
        self._tasks: set = set()
        self._transactions: Dict[str, Transaction] = {}
        self._sessions: Dict[str, Session] = {}

    async def _cancel_tasks(self, tasks):
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def _recv_msg_task(self):
        while True:
            await asyncio.sleep(0.5)
            message = json.loads(await self._websocket.recv())
            if message.get("transaction") is not None:
                transaction = self._transactions.get(message.get("transaction"))
                if transaction is not None:
                    if message["janus"] == "ack":
                        transaction.ack.set_result(True)
                        if transaction.ack_only:
                            del self._transactions[message.get("transaction")]
                    else:
                        transaction.response.set_result(message)
                        del self._transactions[message.get("transaction")]
                else:
                    raise Exception("transaction not exist")
            else:
                pass

    async def connect(self):
        self._websocket: WebSocketCommonProtocol = await websockets.connect(
            self._uri, subprotocols=["janus-protocol"]
        )
        task = self._loop.create_task(self._recv_msg_task())
        self._tasks.add(task)

    async def disconeect(self):
        await self._cancel_tasks()
        await self._websocket.close()

    async def send(self, payload: dict, ack_only: bool = False, timeout=5):
        if self._websocket is None:
            raise Exception("Not connected")
        transaction_id = get_random_id()
        payload["transaction"] = transaction_id
        transaction = Transaction(ack_only=ack_only, loop=self._loop)
        self._transactions[transaction_id] = transaction
        await self._websocket.send(json.dumps(payload))
        return self._transactions[transaction_id]

    async def get_info(self):
        return await self.send({"janus": "info"})

    async def create_session(self, keepalive_timeout=59) -> Session:
        transaction = await self.send({"janus": "create"})
        response = await wait_for(transaction.response, 5)
        if response.get("janus") == "success":
            session_id = response["data"]["id"]
            session = Session(
                session_id, self, loop=self._loop, keepalive_timeout=keepalive_timeout
            )
            self._sessions[session_id] = session
            return session
        raise Exception(json.dumps(response))
