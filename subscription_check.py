import logging
from typing import Any, Awaitable, Callable, Union
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from src.config import settings
from src.database.models import User, UserType
from src.database.session import get_session
from src.services.subscription_service import SubscriptionService
from src.utils.constants import Text, UserKeyboard

logger = logging.getLogger(__name__)


class SubscriptionCheckMiddleware(BaseMiddleware):
    PUBLIC_COMMANDS = {"/start", "/help", "/myinfo"}

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user
        user_id = user.id if user else None
        if user_id is None or await self._is_admin_user(user_id):
            return await handler(event, data)
        if isinstance(event, Message) and event.text and event.text.startswith("/"):
            command = event.text.split()[0].split("@")[0]
            if command in self.PUBLIC_COMMANDS:
                return await handler(event, data)
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)
        bot = data.get("bot")
        if bot and await SubscriptionService.check_subscription(bot, user_id):
            return await handler(event, data)
        if isinstance(event, CallbackQuery):
            await event.answer(Text.SUBSCRIBE_REQUIRED, show_alert=True)
        else:
            await event.answer(Text.SUBSCRIBE_REQUIRED, reply_markup=UserKeyboard.get_subscribe_keyboard())
        return None

    @staticmethod
    async def _is_admin_user(user_id: int) -> bool:
        if user_id in settings.ADMINS:
            return True
        try:
            async with get_session() as session:
                result = await session.execute(select(User.user_type).where(User.telegram_id == user_id))
                return result.scalar_one_or_none() in (UserType.ADMIN, UserType.OWNER)
        except Exception:
            logger.exception("Admin tekshirishda xatolik")
            return False
