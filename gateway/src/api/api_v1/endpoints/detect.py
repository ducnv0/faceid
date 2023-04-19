from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect
import asyncio

from src.utils.common import LOGGER
from src.services.face import service_instance as face_service
from src.settings import settings


router = APIRouter()


@router.post('')
async def detect_faces_rest(file: UploadFile):
    # FIXME: improve this. Avoid directly calling long running blocking operations
    facial_areas = face_service.detect_faces(await file.read())

    return facial_areas
    

# handle back-pressure
@router.websocket('')
async def detect_faces_ws(ws: WebSocket):
    await ws.accept()
    queue = asyncio.Queue(maxsize=settings.WS_QUEUE_MAX_SIZE)

    # submit detection task to the event loop for execution without calling await
    detection_task = asyncio.create_task(detect_faces(ws=ws, queue=queue))
    try:
        while True:
            await receive_img(ws=ws, queue=queue)
    except WebSocketDisconnect:
        # client ends the ws connection
        detection_task.cancel()
        try:
            await ws.close()
        except:
            pass
        

async def receive_img(ws: WebSocket, queue: asyncio.Queue):
    """
    Wait to receive an image from the client then put it to an queue
    """
    while True:
        bytes_img = await ws.receive_bytes()
        try:
            # LOGGER.debug('[ws] Received image: %s KB', len(bytes_img))
            queue.put_nowait(bytes_img)
        except asyncio.QueueFull:
            # drop some frame
            LOGGER.debug('[ws] Dropped received image due to the queue exceeded its capacity')


async def detect_faces(ws: WebSocket, queue: asyncio.Queue):
    """
    Pull images from the image queue, run detections and send results back to the client
    """
    while True:
        bytes_img = await queue.get()
        # LOGGER.debug('[ws] Running detections...')
        # FIXME: improve this. Avoid directly calling long running blocking operations
        results = face_service.detect_faces(bytes_img)
        # LOGGER.debug('[ws] Sending detection results back to the client: %s', results)
        await ws.send_json(results)
