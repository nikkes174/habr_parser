import requests
from bs4 import BeautifulSoup

# 1. URL и заголовки (чтобы сайт не подумал, что это бот)
URL = "https://habr.com/ru/articles/top/daily/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
}

# 2. Получаем HTML страницы
response = requests.get(URL, headers=HEADERS)
html = response.text

# 3. Парсим HTML
soup = BeautifulSoup(html, "html.parser")

# 4. Находим все статьи на странице
articles = soup.find_all("article")

# 5. Обрабатываем каждую статью
for i, article in enumerate(articles, start=1):
    # Заголовок
    title_tag = article.find("a", class_="tm-title__link")
    title = title_tag.text.strip() if title_tag else "Без названия"

    # Просмотры
    views_tag = article.find("span", class_="tm-icon-counter__value")
    views = views_tag.text.strip() if views_tag else "—"

    # Вывод в консоль
    print(f"{i}. {title} | Просмотры: {views}")
