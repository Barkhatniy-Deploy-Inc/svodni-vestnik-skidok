import pytest
from app.scraper import Scraper

def test_extract_price_regex():
    """Тест универсального поиска цены по регулярным выражениям."""
    scraper = Scraper()
    
    # Разные форматы цен
    assert scraper._extract_price_regex("Цена: 15 000 руб.") == 15000.0
    assert scraper._extract_price_regex("Купить за 990₽") == 990.0
    assert scraper._extract_price_regex('<meta itemprop="price" content="12500.50">') == 12500.5
    assert scraper._extract_price_regex('"price": 5400') == 5400.0
    
def test_parse_generic():
    """Тест общего парсера."""
    scraper = Scraper()
    html = """
    <html>
        <head><title>Тестовый товар</title></head>
        <body>
            <h1>Крутой гаджет</h1>
            <span class="price">Цена: 5000 руб</span>
        </body>
    </html>
    """
    data = scraper._parse_generic(html)
    assert data["name"] == "Крутой гаджет"
    assert data["price"] == 5000.0
