from typing import List, Optional
from bot.database.models import Session, Task
from datetime import datetime

def add_task(user_id: int, text: str) -> Task:
    """Добавить новую задачу"""
    session = Session()
    try:
        task = Task(user_id=user_id, text=text)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    finally:
        session.close()

def get_user_tasks(user_id: int, only_active: bool = True) -> List[Task]:
    """Получить задачи пользователя"""
    session = Session()
    try:
        query = session.query(Task).filter(Task.user_id == user_id)
        if only_active:
            query = query.filter(Task.is_completed == False)
        return query.order_by(Task.created_at.desc()).all()
    finally:
        session.close()

def complete_task(user_id: int, task_id: int) -> bool:
    """Отметить задачу выполненной"""
    session = Session()
    try:
        task = session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if task and not task.is_completed:
            task.is_completed = True
            task.completed_at = datetime.now()
            session.commit()
            return True
        return False
    finally:
        session.close()

def delete_task(user_id: int, task_id: int) -> bool:
    """Удалить задачу"""
    session = Session()
    try:
        result = session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).delete()
        session.commit()
        return result > 0
    finally:
        session.close()