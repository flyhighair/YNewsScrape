import csv
from typing import cast

import requests
from bs4 import BeautifulSoup

from .error import FetchHtmlError, HtmlParseError

URL = "https://news.yahoo.co.jp/topics"
"""Yahoo!ニュースのトピック一覧ページのURL"""

CSV_FILE = "ynews.csv"
"""出力先のCSVファイル名"""

NewsList = list[tuple[str, str, str]]
"""ニュース一覧の型"""


def fetch_html() -> requests.models.Response:
    """Yahoo!ニュースのトピック一覧ページのHTMLを取得する"""
    try:
        html = requests.get(URL)
        html.raise_for_status()
    except requests.HTTPError as err:
        raise FetchHtmlError(err.response.text)
    except requests.RequestException as err:
        raise FetchHtmlError(err)
    else:
        return html


def parse_news_list_from_html(html: requests.models.Response) -> NewsList:
    """トピック一覧ページのHTMLからニュース一覧を取得する"""
    # 各トピックのニュース見出しとURL一覧を取得
    soup = BeautifulSoup(html.text, "lxml")
    # トピックごとのdiv要素を取得
    topic_list = soup.select("div.sc-dfVpRl.hwKVrp")
    # HTML構造が変わっている可能性があるので例外を発生させる
    if not topic_list:
        raise HtmlParseError
    result_list: NewsList = []

    for topic in topic_list:
        topic_link = topic.select_one("p > a")
        # HTML構造が変わっている可能性があるので例外を発生させる
        if topic_link is None:
            raise HtmlParseError
        topic_name = topic_link.text
        # トピック内のニュース一覧を取得
        news_list = topic.select("ul > li")

        for news in news_list:
            news_link = news.select_one("a")
            if news_link is None:
                # HTML構造が変わっている可能性があるので例外を発生させる
                raise HtmlParseError
            news_title = news_link.text
            # NOTE: href属性のリンクは確実に1つのため、リストではなく文字列にキャストする
            news_url = cast(str, news_link.get("href"))
            news_info = (topic_name, news_title, news_url)
            result_list.append(news_info)

    return result_list


def create_csv(news_list: NewsList) -> None:
    """ニュース一覧をCSVファイルに出力する"""
    with open(CSV_FILE, "w", encoding="UTF-8", newline="") as f:
        csv_writer = csv.writer(f)
        header = ("トピック", "ニュースタイトル", "URL")
        csv_writer.writerow(header)
        csv_writer.writerows(news_list)


def main() -> None:
    """Yahooニュースのスクレイピングを行う"""
    html = fetch_html()
    news_list = parse_news_list_from_html(html)
    create_csv(news_list)


if __name__ == "__main__":
    main()
