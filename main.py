"""
Bot main fayli - Dispatcher va middleware setup
"""
import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from src.config import settings
from src.database.connection import init_db, close_db, async_session
from src.middleware.subscription_check import SubscriptionCheckMiddleware
from src.database.models import User, UserType
from sqlalchemy import select
from src.routers import admin, user, subscription, common, echo_handler

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def load_database_admins():
    """Database adminlarini konfiguratsiya ro‘yxatiga qo‘shadi."""
    async with async_session() as session:
        result = await session.execute(
            select(User.telegram_id).where(
                User.user_type.in_([UserType.ADMIN, UserType.OWNER])
            )
        )
        for telegram_id in result.scalars():
            if telegram_id not in settings.ADMINS:
                settings.ADMINS.append(telegram_id)


async def set_commands(bot: Bot):
    """Bot kommandalarini o'rnatish"""
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam olish"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Bot ishga tushirish"""
    
    # Database init
    logger.info("Database initializatsiyasi...")
    await init_db()
    await load_database_admins()
    
    # Bot va Dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Routers qo'shish
    dp.include_router(subscription.router)
    dp.include_router(common.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(echo_handler.router)
    
    # Middleware qo'shish (admin handlers oldidan)
    dp.message.middleware(SubscriptionCheckMiddleware())
    dp.callback_query.middleware(SubscriptionCheckMiddleware())
    
    # Kommandalarni o'rnatish
    await set_commands(bot)
    
    try:
        logger.info("Bot ishga tushurildi...")
        await dp.start_polling(bot)
    finally:
        await close_db()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())