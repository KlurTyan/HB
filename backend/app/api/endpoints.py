import json

from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from app.manager import get_db

from db.models import User, Task, SystemLog

from app.core.ws_manager import ws_manager

router = APIRouter(prefix='/api', tags=['api'])

poll_state = {
    "is_active": False,
    "fire": 0,
    "cringe": 0,
    "voted_users": set()
}

@router.post("/admin/poll/start")
async def start_poll():
    await ws_manager.broadcast(json.dumps({"type": "start_poll"}))
    poll_state["is_active"] = True
    poll_state["voted_users"].clear()
    poll_state["fire"] = 0
    poll_state["cringe"] = 0
    return {"status": "started"}

@router.post("/admin/poll/stop")
async def stop_poll():
    poll_state["is_active"] = False
    result_msg = f"📊 Итоги: 🔥 Огонь: {poll_state['fire']} | 🎤 Кринж: {poll_state['cringe']}"
    await ws_manager.broadcast(json.dumps({"type": "stop_poll", "message": result_msg}))
    return {"status": "stopped", "results": poll_state}

@router.post("/react")
async def handle_reaction(reaction: dict): # {type: 'fire'}
    token = reaction.get("token")
    if poll_state["is_active"]:
        if poll_state["is_active"] and token not in poll_state["voted_users"]:
            poll_state["voted_users"].add(token)
        poll_state[reaction['type']] += 1
    return {"status": "ok"}

@router.get("/profile/{token}")
async def get_me(token: str, db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(User).options(selectinload(User.tasks)).where(User.token == token)
    result = (await db.execute(query)).scalars().first()
    can_vote = poll_state["is_active"] and (token not in poll_state["voted_users"])

    return {
        "id": result.id,
        "name": result.name,
        "role": result.role,
        "token": result.token,
        "secret_char": result.secret_char,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed
            } for task in result.tasks
        ],
        "poll_active": can_vote
    }

@router.get("/tasks")
async def get_tasks(user_id: int, db: Annotated[AsyncSession, Depends(get_db)], ):
    query = select(User).options(selectinload(User.tasks)).where(User.id == user_id)
    result = (await db.execute(query)).scalars().first()

    return {"tasks" : result.tasks}

@router.post("/complete-task")
async def completed_task(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    tasks_query = select(Task).options(selectinload(Task.tasks_user)).where(and_(Task.id == task_id, ~Task.is_completed))
    task = (await db.execute(tasks_query)).scalars().first()

    if not task:
        return "No task"

    log_deploy = f"[DEPLOY] {task.tasks_user.name} успешно развернул подсистему '{task.title}'"

    await ws_manager.broadcast(log_deploy)
    db.add(SystemLog(message=log_deploy))

    task.is_completed = True

    total_query = select(func.count(Task.id)).where(Task.user_id == task.user_id)
    completed_query = select(func.count(Task.id)).where(
        Task.user_id == task.user_id,
        Task.is_completed == True
    )

    total_count = (await db.execute(total_query)).scalar()
    completed_count = (await db.execute(completed_query)).scalar()

    if total_count == completed_count:
        log_success = f"[SUCCESS] {task.tasks_user.role} ({task.tasks_user.name}) синхронизирован с основным ядром!"
        await ws_manager.broadcast(log_success)
        db.add(SystemLog(message=log_success))
    return {"message": "Task completed!"}