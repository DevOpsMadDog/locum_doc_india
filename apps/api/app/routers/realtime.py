from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.realtime import manager

router = APIRouter(prefix="/ws", tags=["realtime"])


@router.websocket("/assignments/{assignment_id}")
async def assignment_socket(websocket: WebSocket, assignment_id: int) -> None:
    room = f"assignment:{assignment_id}"
    await manager.connect(room, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
