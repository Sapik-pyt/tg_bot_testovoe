from db import User
from db_deploy import session
from sqlalchemy import select


async def create_user(
        user_id: int, first_name: str,
        last_name: str, email: str,
        phone: str, birth_day: int, status: str):
    user = User(
        id=user_id, first_name=first_name, last_name=last_name,
        email=email, phone_number=phone,
        birth_day=birth_day, status=status
    )
    session.add(user)
    session.commit()


async def select_user(user_id: int) -> bool:
    user = select.filter(User.id == user_id).first()
    return user
