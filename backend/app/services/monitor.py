import asyncio
import logging
import random
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import AsyncSessionLocal
from ..models import Product, PriceHistory, User
from ..scraper import Scraper
from ..core.telegram import send_notification

logger = logging.getLogger(__name__)
scraper = Scraper()

async def check_all_prices():
    """
    Основная функция обхода всех товаров и проверки цен с паузами.
    """
    logger.info("Начало плановой проверки цен...")
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        
        for product in products:
            try:
                # Добавляем случайную паузу от 3 до 10 секунд между товарами
                wait_time = random.uniform(3, 10)
                await asyncio.sleep(wait_time)
                
                # Получаем новые данные
                data = await scraper.get_product_data(product.url)
                new_price = data.get("price")
                
                if new_price is not None:
                    # Если цена изменилась, записываем в историю
                    if new_price != product.current_price:
                        history_entry = PriceHistory(
                            product_id=product.id,
                            price=new_price
                        )
                        db.add(history_entry)
                        
                        # Проверяем, достигла ли цена желаемого уровня
                        if product.target_price and new_price <= product.target_price:
                            await notify_user(db, product, new_price)
                        
                        # Обновляем текущую цену в карточке товара
                        product.current_price = new_price
                        product.name = data.get("name", product.name)
            
            except Exception as e:
                logger.error(f"Ошибка при проверке товара {product.id}: {e}")
        
        await db.commit()
    logger.info("Проверка цен завершена.")

async def notify_user(db: AsyncSession, product: Product, price: float):
    """
    Логика формирования и отправки уведомления.
    """
    # Получаем информацию о владельце товара
    user_result = await db.execute(select(User).where(User.id == product.user_id))
    user = user_result.scalars().first()
    
    if user:
        message = (
            f"🔔 <b>Скидка обнаружена!</b>\n\n"
            f"Товар: <a href='{product.url}'>{product.name}</a>\n"
            f"Текущая цена: <b>{price} ₽</b>\n"
            f"Ваша цель: {product.target_price} ₽"
        )
        await send_notification(user.telegram_id, message)
