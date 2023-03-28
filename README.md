# YNewsScrape

Script for scraping Yahoo News.

## Requirement

- Python ^3.11
- Poetry
- GNU make

## Installation

```sh
git clone https://github.com/flyhighair/ynewsscrape.git
cd ynewsscrape
poetry install
```

## Usage

Execution command

```sh
make run
# or
poetry run python -m ynewsscrape
```

After executing the command, the following results will be written to the ynews.csv file.

```csv
トピック,ニュースタイトル,URL
国内,114兆円超 23年度予算が成立,https://news.yahoo.co.jp/pickup/6458430
...
```
