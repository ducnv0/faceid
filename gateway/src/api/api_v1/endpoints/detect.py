from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.concurrency import run_in_threadpool
import asyncio

from src.services.face import service_instance as face_service
from src.settings import settings
from src.utils.common import LOGGER
from src.exceptions.websocket import WebsocketSendError


router = APIRouter()


@router.post('')
async def detect_rest(
    file: UploadFile,
    identity: bool = False
):
    bytes_img = await file.read()
    if identity:
        if not face_service.embeddings_loaded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Model is not trained'
            )
        return await run_in_threadpool(face_service.recognize, bytes_img)
    return await run_in_threadpool(face_service.detect, bytes_img)


# handle back-pressure
@router.websocket('')
async def detect_ws(ws: WebSocket, identity: bool = False):
    await ws.accept()
    if identity:
        if not face_service.embeddings_loaded:
            await ws.send_text('Model is not trained')
            await ws.close()

    queue = asyncio.Queue(maxsize=settings.WS_QUEUE_MAX_SIZE)

    # submit receive task to the event loop for execution without calling await
    receive_task = asyncio.create_task(face_service.receive_imgs_helper(ws=ws, queue=queue))

    try:
        await face_service.detect_faces_helper(ws=ws, queue=queue, identity=identity)
    except (WebSocketDisconnect, WebsocketSendError):
        # client ends the ws connection
        LOGGER.debug('[ws] Client Closed')
        receive_task.cancel()
        try:
            await ws.close()
        except:
            pass
