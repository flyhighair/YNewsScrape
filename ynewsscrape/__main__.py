#!/usr/bin/env python
# coding: utf-8

import os
import time

from .ynewsscrape import scrape

INTERVAL_SECONDS = 3
"""スクリプト実行間隔(秒)"""


def main():
    # 前回の実行時間を取得する
    if os.path.exists("last_run_time.txt"):
        with open("last_run_time.txt", "r") as f:
            last_run_time = float(f.read().strip())
    else:
        last_run_time = 0.0

    with open("last_run_time.txt", "w") as f:
        current_time = time.time()
        f.write(str(current_time))

    # 負荷をかけないよう、前回の実行時間から3秒以上経ってからスクレイピングを行う
    if current_time - last_run_time < INTERVAL_SECONDS:
        time.sleep(INTERVAL_SECONDS - (current_time - last_run_time))

    scrape()


if __name__ == "__main__":
    main()
