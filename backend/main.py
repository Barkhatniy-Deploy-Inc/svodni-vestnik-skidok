import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# --- Настройка логирования ---
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Запись в файл (до 5 МБ, храним 5 последних копий)
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setFormatter(log_formatter)

# Вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
logger = logging.getLogger("price_sentinel")

# Импорты приложения после настройки логов
from app.database import engine, Base
from app.api import products
from app.services.monitor import check_all_prices
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

app = FastAPI(
    title="Price Sentinel API",
    description="API для системы мониторинга цен (Сводный Вестник Скидок)",
    version="0.1.0"
)

# Инициализация планировщика
scheduler = AsyncIOScheduler()

# Настройка CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(products.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    logger.info("Запуск приложения...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Проверка цен каждые 4 часа
    scheduler.add_job(check_all_prices, "interval", hours=4)
    scheduler.start()
    logger.info("Планировщик запущен: проверка цен каждые 4 часа.")

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    logger.info("Приложение остановлено.")

@app.get("/", tags=["Общее"])
async def root():
    logger.info("Запрос к корневому эндпоинту")
    return {"message": "Добро пожаловать в API Сводного Вестника Скидок"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Запуск сервера uvicorn на порту 8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
