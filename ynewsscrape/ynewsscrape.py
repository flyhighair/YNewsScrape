import csv
import logging

import requests
from bs4 import BeautifulSoup

URL = "https://news.yahoo.co.jp/topics"


def main():
    html = requests.get(URL)
    try:
        html.raise_for_status()
    except requests.HTTPError as err:
        logging.error("request failed. error=%s", err.response.text)
        return

    # bs4でパースし、各トピックのニュース見出しとURL一覧を取得
    soup = BeautifulSoup(html.text, "lxml")
    # トピックごとのdivを取得
    topic_list = soup.select("div.sc-dfVpRl.hwKVrp")
    news_data = []
    for topic in topic_list:
        topic_name = topic.select_one("p > a").text
        # トピック内のニュース一覧を取得
        news_list = topic.select("ul > li")
        for news in news_list:
            news_title = news.select_one("a").text
            news_url = news.select_one("a").get("href")
            news_data.append([topic_name, news_title, news_url])
    # ニュース一覧をCSVに書き出す
    csv_file = "ynews.csv"
    with open(csv_file, "w", encoding="UTF-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["トピック", "ニュースタイトル", "URL"])
        csv_writer.writerows(news_data)


if __name__ == "__main__":
    main()
