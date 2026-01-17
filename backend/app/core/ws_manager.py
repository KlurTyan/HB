import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        if not self.active_connections:
            return

        tasks = [connection.send_text(message) for connection in self.active_connections]
        results = await asyncio.gather(*tasks, return_exceptions=True)

ws_manager =  ConnectionManager()