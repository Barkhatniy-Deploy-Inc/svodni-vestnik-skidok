import httpx
from bs4 import BeautifulSoup
import logging
import re
import json
from urllib.parse import urlparse

# Настройка логирования
logger = logging.getLogger(__name__)

class Scraper:
    """
    Класс для сбора данных о ценах.
    Включает специфичную логику для Ozon, WB и Яндекс Маркета.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }

    async def get_product_data(self, url: str) -> dict:
        """
        Определяет домен и вызывает соответствующий метод парсинга.
        """
        try:
            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True, timeout=15.0) as client:
                response = await client.get(url)
                if response.status_code != 200:
                    logger.error(f"Ошибка загрузки {url}: статус {response.status_code}")
                    return {"name": "Ошибка доступа", "price": None}
                
                domain = urlparse(url).netloc
                html = response.text
                
                if "wildberries.ru" in domain:
                    return self._parse_wildberries(html)
                elif "ozon.ru" in domain:
                    return self._parse_ozon(html)
                elif "market.yandex.ru" in domain:
                    return self._parse_yandex(html)
                else:
                    return self._parse_generic(html)
        except Exception as e:
            logger.error(f"Исключение при парсинге {url}: {e}")
            return {"name": "Ошибка системы", "price": None}

    def _parse_wildberries(self, html: str) -> dict:
        """Парсинг Wildberries через поиск JSON в скриптах или мета-тегах."""
        soup = BeautifulSoup(html, "html.parser")
        name = soup.find("h1")
        name_text = name.get_text(strip=True) if name else "Товар Wildberries"
        
        # WB часто хранит данные в SSR JSON. Пытаемся найти цену в мета-тегах.
        price_meta = soup.find("meta", property="product:price:amount")
        price = float(price_meta["content"]) if price_meta else self._extract_price_regex(html)
        
        return {"name": name_text, "price": price}

    def _parse_ozon(self, html: str) -> dict:
        """Парсинг Ozon (сложный случай, ищем JSON-LD)."""
        soup = BeautifulSoup(html, "html.parser")
        
        # Ищем заголовок
        name_tag = soup.find("h1")
        name = name_tag.get_text(strip=True) if name_tag else "Товар Ozon"
        
        # Ozon часто прячет цену в скриптах ld+json
        price = None
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and "offers" in data:
                    price = data["offers"].get("lowPrice") or data["offers"].get("price")
                    if price: break
            except: continue
            
        if not price:
            price = self._extract_price_regex(html)
            
        return {"name": name, "price": float(price) if price else None}

    def _parse_yandex(self, html: str) -> dict:
        """Парсинг Яндекс Маркета."""
        soup = BeautifulSoup(html, "html.parser")
        name = soup.find("h1")
        name_text = name.get_text(strip=True) if name else "Товар Яндекс Маркет"
        
        # Ищем цену в специфичных тегах или мета-данных
        price_meta = soup.find("meta", itemprop="price")
        price = price_meta["content"] if price_meta else self._extract_price_regex(html)
        
        return {"name": name_text, "price": float(price) if price else None}

    def _parse_generic(self, html: str) -> dict:
        """Универсальный парсер для остальных сайтов."""
        soup = BeautifulSoup(html, "html.parser")
        name = soup.find("h1") or soup.find("title")
        name_text = name.get_text(strip=True) if name else "Неизвестный товар"
        
        price = self._extract_price_regex(html)
        return {"name": name_text, "price": price}

    def _extract_price_regex(self, html: str) -> float | None:
        """Улучшенный поиск цены регулярными выражениями."""
        # Очищаем HTML от скриптов, чтобы не найти лишние цифры
        clean_text = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
        clean_text = re.sub(r'<style.*?>.*?</style>', '', clean_text, flags=re.DOTALL)
        
        # Ищем конструкции типа 15 990 руб, 15990₽, 15.990,00
        patterns = [
            r'(\d[\d\s\xa0]*)\s?[₽руб]', # 15 000 руб
            r'price["\']\s?:\s?(\d+)',    # "price": 15000
            r'itemprop=["\']price["\']\s+content=["\'](\d+[\d\.]*)["\']', # itemprop="price" content="12500"
            r'content=["\'](\d+[\d\.]*)["\']\s+itemprop=["\']price["\']'  # content="12500" itemprop="price"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                price_str = match.group(1).replace(" ", "").replace("\xa0", "").replace(",", ".")
                try:
                    # Убираем лишние точки, если это разделители тысяч
                    if price_str.count('.') > 1:
                        price_str = price_str.replace('.', '')
                    return float(price_str)
                except ValueError:
                    continue
        return None
