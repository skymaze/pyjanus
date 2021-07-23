class Transaction:
    def __init__(self, loop, ack_only: bool = False) -> None:
        self._loop = loop
        self.ack_only = ack_only
        self.ack = self._loop.create_future()
        self.response = self._loop.create_future()
