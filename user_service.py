"""User operations."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, UserType


class UserService:
    @staticmethod
    async def get_or_create(session: AsyncSession, telegram_id: int) -> User:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.flush()
        return user

    @staticmethod
    async def is_admin(session: AsyncSession, telegram_id: int) -> bool:
        user = await UserService.get_or_create(session, telegram_id)
        return user.user_type in (UserType.ADMIN, UserType.OWNER)

    @staticmethod
    async def set_admin(session: AsyncSession, telegram_id: int, is_admin: bool):
        user = await UserService.get_or_create(session, telegram_id)
        user.user_type = UserType.ADMIN if is_admin else UserType.USER
        await session.flush()

    @staticmethod
    async def count_users(session: AsyncSession) -> int:
        result = await session.execute(select(func.count(User.id)))
        return result.scalar_one()
