from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from config import HEADERS


class BaseParser(ABC):
    @abstractmethod
    def get_result(self) -> None:
        pass


class HTMLParser(BaseParser):
    def __init__(self, url: str | None, selector: str | None):
        self.headers: dict[str, str] = HEADERS
        self.url: Optional[str] = url
        self.selector: Optional[str] = selector

    def input_url(self) -> None:
        while True:
            try:
                introduced_url = input('Введите URL: ').strip()

                if not introduced_url:
                    raise ValueError('Вы ничего не ввели')

                self.url = introduced_url
                break
            except ValueError as e:
                print(f'{e}. Попробуйте ввод снова')

    def input_selector(self) -> None:
        while True:
            try:
                introduced_selector = input('Введите нужный элемент: ')
                if not introduced_selector:
                    raise ValueError('Вы ничего не ввели')

                self.selector = introduced_selector
                break
            except ValueError as e:
                print(f'{e}. Попробуйте ввод снова')

    def get_result(self) -> None:
        html: str = requests.get(self.url, headers=self.headers).text
        articles: list[Tag] = BeautifulSoup(html, "html.parser").find_all(
            'article'
        )

        for i, article in enumerate(articles, start=1):
            title: str = (article.find("a", class_=self.selector).text.strip()
                          if article.find("a", class_=self.selector)
                          else "Без названия")
            views: str = (article.find("span", class_="tm-icon-counter__value").text.strip()
                          if article.find("span", class_="tm-icon-counter__value")
                          else "—")
            print(f'{i}. {title} | Просмотры: {views}')
