from typing import Annotated

from fastapi import WebSocket, APIRouter

from ..db.models import User, Task, Reactions, SystemLog
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.ws_manager import ws_manager

from app.manager import get_db

import asyncio

router = APIRouter(prefix="/ws", tags=["Websocket"])

@router.websocket("/logs")
async def reaction(ws: WebSocket, db: Annotated[AsyncSession, Depends(get_db)]):
    await ws_manager.connect(ws)
    try:
        logs_query = select(SystemLog).order_by(SystemLog.id.asc())
        result = (await db.execute(logs_query)).scalars().all()
        for log in result:
            await ws.send_text(log.message)
        while True:
            await ws.receive_text()
    except Exception:
        ws_manager.disconnect(ws)