from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# Базовая схема для товара
class ProductBase(BaseModel):
    url: HttpUrl # Ссылка на товар
    target_price: Optional[float] = None # Желаемая цена для уведомления

# Схема для создания товара
class ProductCreate(ProductBase):
    pass

# Схема для отображения товара
class ProductRead(ProductBase):
    id: int
    name: str
    current_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Схема для истории цен
class PriceHistoryRead(BaseModel):
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True

# Полная информация о товаре с историей цен
class ProductDetail(ProductRead):
    price_history: List[PriceHistoryRead]

# Схемы для пользователя
class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
