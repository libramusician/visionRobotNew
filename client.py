import websockets


class Client:
    def __init__(self, websocket):
        print(type(websocket))
        self.websocket = websocket

    async def response(self, msg):
        try:
            await self.websocket.send(msg)
        except websockets.ConnectionClosed:
            print("connection closed while sending, abort")
