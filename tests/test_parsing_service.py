import os
import sys
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsing_service import HTMLParser


@patch(
    "builtins.input", side_effect=["https://habr.com/ru/articles/top/daily/"]
)
def test_input_url(mock_input: Any) -> None:
    parser = HTMLParser(None, None)
    parser.input_url()
    assert parser.url == "https://habr.com/ru/articles/top/daily/"


@patch("builtins.input", side_effect=["tm-title__link"])
def test_input_selector(mock_input: Any) -> None:
    parser = HTMLParser(None, None)
    parser.input_selector()
    assert parser.selector == "tm-title__link"


@patch("requests.get")
def test_get_result_parses_articles(
    mock_get: MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_html = """
    <html>
        <body>
            <article>
                <a class="tm-title__link"><span>Первая статья</span></a>
                <span class="tm-icon-counter__value">1.2K</span>
            </article>
            <article>
                <a class="tm-title__link"><span>Вторая статья</span></a>
                <span class="tm-icon-counter__value">3.4K</span>
            </article>
        </body>
    </html>
    """
    mock_get.return_value.text = fake_html

    parser = HTMLParser("https://fake-url", "tm-title__link")
    parser.get_result()

    captured = capsys.readouterr()
    output = captured.out.strip()

    assert "1. Первая статья | Просмотры: 1.2K" in output
    assert "2. Вторая статья | Просмотры: 3.4K" in output


@patch("requests.get")
def test_get_result_handles_missing_tags(
    mock_get: MagicMock, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_html = "<html><body><article></article></body></html>"
    mock_get.return_value.text = fake_html

    parser = HTMLParser("https://fake-url", "tm-title__link")
    parser.get_result()

    captured = capsys.readouterr()
    output = captured.out.strip()

    assert "1." in output


def test_get_result_raises_error_when_no_url() -> None:
    parser = HTMLParser(None, "tm-title__link")

    with pytest.raises(ValueError):
        parser.get_result()
