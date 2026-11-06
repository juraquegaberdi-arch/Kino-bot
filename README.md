# 🎬 Kino Bot

Telegram bot — kino kodlari orqali videolarni yuborish, majburiy kanal obunasi va admin panel.

## ✨ Xususiyatlari

✅ **Mandatory Channel Subscription** - Foydalanuvchiar botdan oldin kanallarga obuna bo'lishlari kerak
✅ **Admin Panel** - Kinolarni qo'shish, o'chirish, ro'yxatini ko'rish
✅ **Movie Code System** - Kod orqali kino linkini olish
✅ **Database** - PostgreSQL + SQLAlchemy (async)
✅ **Docker Support** - Docker + docker-compose orqali deploy
✅ **Professional Code** - Middleware, FSM, Router-based architecture

## 🚀 Tezkor Start

### 1. Prerequisites
- Python 3.10+
- PostgreSQL
- Docker + Docker Compose (optional)

### 2. Setup (Local)

```bash
# Repository clone
git clone https://github.com/yourusername/kino-bot.git
cd kino-bot

# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\\Scripts\\activate  # Windows

# Dependencies install
pip install -r requirements.txt

# .env fayli yaratish
cp .env.example .env
# .env ni o'zingizning malumotlari bilan to'ldiring

# Database yaratish
# (PostgreSQL server ishga tushurilgan bo'lishi kerak)

# Botni ishga tushirish
python -m src.main
```

### 3. Setup (Docker)

```bash
# .env fayli yaratish
cp .env.example .env
# Zaruriy konfiguratsiyani o'zgartiring

# Docker Compose orqali ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f bot
```

## 📋 Loyiha Strukturasi

```
kino_bot/
├── src/
│   ├── config.py                 # Settings
│   ├── main.py                   # Bot entry point
│   ├── database/
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── connection.py         # DB connection
│   │   └── session.py            # Session manager
│   ├── services/
│   │   ├── movie_service.py      # Movie CRUD
│   │   ├── user_service.py       # User operations
│   │   └── subscription_service.py # Subscription check
│   ├── routers/
│   │   ├── admin.py              # Admin handlers
│   │   ├── user.py               # User handlers
│   │   └── subscription.py       # Subscription handlers
│   ├── middleware/
│   │   └── subscription_check.py # Mandatory subscribe
│   └── utils/
│       └── constants.py          # Constants, keyboards
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ⚙️ Konfiguratsiya (.env)

```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/kino_bot
SUBSCRIPTION_CHANNELS=-1001234567890,-1001234567891
ADMINS=123456789,987654321
DEBUG=False
```

### Channel ID olamiz:
1. @userinfobot ga /start yuboring
2. Targetinizni channel ga qo'shib, message yuboring
3. @userinfobot ga message forward qiling
4. Olingan ID ni (minus belgisi bilan) SUBSCRIPTION_CHANNELS ga qo'ying

## 👨‍💼 Admin Panel

Admin panelga (/admin) kirish:
- **Kino qo'shish** - Kod va URL bog'lash
- **Kino o'chirish** - Kodni kiritib o'chirish
- **Ro'yxat** - Barcha kinolarni ko'rish
- **Bekor** - Amaldan chiqish

Adminlar ADMINS env variable da belgilangan Telegram ID lar.

## 👤 User Harakat

1. /start - Botni ishga tushirish
2. Kanallarni ko'rish va obuna bo'lish
3. "Tekshirish" tugmasini bosish
4. Kino kodini kiritish
5. Kino linkini olish

## 🗄️ Database Models

### Users Table
- id (PK)
- telegram_id (unique)
- is_admin (boolean)
- created_at (datetime)

### Movies Table
- id (PK)
- code (unique)
- message_id (Telegram file_id yoki chat_id:message_id)
- caption (text, optional)
- created_at (datetime)

## 🔧 Middleware Architecture

**SubscriptionCheckMiddleware** - Har qanday message/callback oldidan obunani tekshirish

Admin callback-lar (add_movie, delete_movie, list_movies) middleware orqali skip qilinadi.

## 📡 FSM (Finite State Machine)

### UserStates
- waiting_for_code - Kino kodi kutish

### AdminStates
- waiting_for_movie_code - Kino kodi kutish
- waiting_for_movie_url - Kino URL kutish
- waiting_for_delete_code - O'chirish uchun kod kutish

## 🐛 Troubleshooting

**"Database connection error"**
- PostgreSQL server ishga tushurilganini tekshiring
- DATABASE_URL ning to'g'riligini tekshiring

**"Invalid token"**
- BOT_TOKEN ni to'g'ri kiritganingizni tekshiring

**"Channel ID not found"**
- Channel ID ni to'g'ri formatda (-1001234567890) kiritganingizni tekshiring

## 📦 Kerakli Tools

- [BotFather](https://t.me/BotFather) - Bot token olish
- [@userinfobot](https://t.me/userinfobot) - Channel ID olish
- PostgreSQL 13+
- Docker (optional)

## 📝 Licenseya

MIT License - ushbu proyektni ochiq shaklda ishlatishingiz mumkin.

## 🤝 Qo'llab-quvvatlash

Agar savol bo'lsa yoki bug topsa, GitHub issues orqali xabar bering.

## Muhim eslatma

Bot ishga tushishidan oldin `.env` faylida haqiqiy `BOT_TOKEN`, admin Telegram ID’lari va kanal ID’larini kiriting. Bot kanal obunasini tekshirishi uchun Telegram kanallarida botni administrator qilib qo‘ying. `ADMINS` va `SUBSCRIPTION_CHANNELS` qiymatlari vergul bilan ajratilgan formatda qabul qilinadi.

Docker orqali ishga tushirganda bot `CMD ["python", "-m", "src.main"]` komandasi bilan avtomatik boshlanadi.
