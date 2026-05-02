from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

clients = set()

current_state = {
    "running": False,
    "session_id": None,
    "session_dir": None,
    "scenario": None,
    "position_id": None,
    "repeat_count": None,
    "current_action": None,
    "message": "Idle",
    "camera_ready": False,
    "csi_ready": False,
    "error": None,
}


async def broadcast_state():
    print("BROADCAST TO CLIENTS:", len(clients), current_state)

    dead_clients = []

    for client in clients:
        try:
            await client.send_json(current_state)
        except Exception:
            dead_clients.append(client)

    for client in dead_clients:
        clients.discard(client)


@router.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    print("WS CONNECTED:", len(clients))

    try:
        await websocket.send_json(current_state)

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        clients.discard(websocket)
        print("WS DISCONNECTED:", len(clients))