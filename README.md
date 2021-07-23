# pyjanus
janus-gateway python client

## Usage
```
from pyjanus import Client
from pyjanus.plugins.videoroom import ListparticipantsRequest

client = Client('wss://janus.conf.meetecho.com/ws')
await client.connect()

session = await client.create_session(keepalive_timeout=9)
handle = await session.attach("janus.plugin.videoroom")

# send request
tr = await handle.send({"request": "list"})
response = await tr.response

# send request use plugin model
tr = await handle.send(ListparticipantsRequest(room=1234).dict(exclude_none=True))
response = await tr.response
```