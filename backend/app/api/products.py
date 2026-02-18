from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ..database import get_db
from .. import models, schemas, scraper
from ..core.auth import get_current_user_id
from datetime import datetime, timedelta
import asyncio

router = APIRouter(
    prefix="/products",
    tags=["Товары"],
    responses={404: {"description": "Товар не найден"}},
)

# Инициализация парсера
product_scraper = scraper.Scraper()

# Глобальная переменная для хранения времени последнего ручного обновления
last_manual_update = None

import logging
logger = logging.getLogger("price_sentinel.api")

@router.post("/", response_model=schemas.ProductRead, summary="Добавить новый товар")
async def create_product(
    product: schemas.ProductCreate, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Добавляет товар в список наблюдения.
    Сразу вызывает парсер для получения названия и текущей цены.
    """
    logger.info(f"Пользователь {user_id} пытается добавить товар: {product.url}")
    
    # Получаем актуальные данные с сайта
    try:
        scraped_data = await product_scraper.get_product_data(str(product.url))
        logger.info(f"Результат парсинга: {scraped_data}")
    except Exception as e:
        logger.error(f"Критическая ошибка парсера при добавлении: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ошибка парсера: {str(e)}")
    
    if scraped_data.get("price") is None:
        logger.warning(f"Парсер не смог найти цену по ссылке: {product.url}")
        # Мы всё равно сохраняем товар, но уведомляем пользователя
    
    new_product = models.Product(
        url=str(product.url),
        name=scraped_data.get("name", "Неизвестный товар"),
        target_price=product.target_price,
        current_price=scraped_data.get("price"),
        user_id=user_id
    )
    
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    # Если цена была получена, сохраняем её в историю
    if new_product.current_price is not None:
        history_entry = models.PriceHistory(
            product_id=new_product.id,
            price=new_product.current_price
        )
        db.add(history_entry)
        await db.commit()
        
    return new_product

@router.get("/", response_model=List[schemas.ProductRead], summary="Получить список всех товаров")
async def read_products(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """ Возвращает список всех товаров пользователя. """
    result = await db.execute(
        select(models.Product)
        .where(models.Product.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/update-all", summary="Запустить обновление цен вручную")
async def update_all_prices():
    """
    Запускает фоновую задачу обновления всех цен.
    Ограничение: не чаще одного раза в 2 часа.
    """
    global last_manual_update
    
    now = datetime.now()
    if last_manual_update and now < last_manual_update + timedelta(hours=2):
        remaining = (last_manual_update + timedelta(hours=2)) - now
        minutes = int(remaining.total_seconds() // 60)
        raise HTTPException(
            status_code=429, 
            detail=f"Слишком часто! Попробуйте снова через {minutes} мин."
        )
    
    from ..services.monitor import check_all_prices
    # Запускаем проверку как фоновую задачу, чтобы не заставлять пользователя ждать
    asyncio.create_task(check_all_prices())
    
    last_manual_update = now
    return {"status": "success", "message": "Обновление цен запущено в фоновом режиме"}

@router.get("/{product_id}", response_model=schemas.ProductDetail, summary="Получить детали товара")
async def read_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """ Возвращает подробную информацию о товаре, включая историю изменения цен. """
    result = await db.execute(
        select(models.Product).where(
            models.Product.id == product_id,
            models.Product.user_id == user_id # Проверка владельца
        )
    )
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден или доступ запрещен")
    return product

@router.delete("/{product_id}", summary="Удалить товар")
async def delete_product(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """ Прекращает наблюдение за товаром и удаляет его из базы. """
    result = await db.execute(
        select(models.Product).where(
            models.Product.id == product_id,
            models.Product.user_id == user_id # Проверка владельца
        )
    )
    product = result.scalars().first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден или доступ запрещен")
    
    await db.delete(product)
    await db.commit()
    return {"status": "success", "message": "Товар удален из списка наблюдения"}
