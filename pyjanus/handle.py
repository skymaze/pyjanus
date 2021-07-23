from pyee import AsyncIOEventEmitter


class Handle(AsyncIOEventEmitter):
    def __init__(self, handle_id: str, session, loop):
        super().__init__(loop=loop)
        self._handle_id = handle_id
        self._session = session

    async def send(self, body, jsep=None, timeout=5):
        payload = {"janus": "message", "body": body}
        payload["handle_id"] = self._handle_id
        if jsep is not None:
            payload["jsep"] = jsep
        return await self._session.send(payload, timeout=timeout)

    async def on_handle_message(self, message):
        self.emit("message", message)
