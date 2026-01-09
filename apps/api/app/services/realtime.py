from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room, set()).add(websocket)

    def disconnect(self, room: str, websocket: WebSocket) -> None:
        if room in self.active_connections:
            self.active_connections[room].discard(websocket)

    async def broadcast(self, room: str, message: dict) -> None:
        for connection in self.active_connections.get(room, set()):
            await connection.send_json(message)


manager = ConnectionManager()
