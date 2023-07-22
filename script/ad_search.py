from sqlite3 import Connection, Cursor
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
from datetime import datetime

from selenium.webdriver.remote.webelement import WebElement

olx_url = "https://www.olx.ua/d/uk/transport/legkovye-avtomobili/vaz/kiev/?currency=UAH&search%5Bdist%5D=5&search" \
          "%5Bfilter_enum_model%5D%5B0%5D=2108&search%5Bfilter_enum_model%5D%5B10%5D=2108i&search%5Bfilter_enum_model" \
          "%5D%5B11%5D=21091&search%5Bfilter_enum_model%5D%5B1%5D=21093&search%5Bfilter_enum_model%5D%5B2%5D=21096" \
          "&search%5Bfilter_enum_model%5D%5B3%5D=21099i&search%5Bfilter_enum_model%5D%5B4%5D=21099&search" \
          "%5Bfilter_enum_model%5D%5B5%5D=2109i&search%5Bfilter_enum_model%5D%5B6%5D=2109&search%5Bfilter_enum_model" \
          "%5D%5B7%5D=21081&search%5Bfilter_enum_model%5D%5B8%5D=21083&search%5Bfilter_enum_model%5D%5B9%5D=21086" \
          "&search%5Bfilter_float_price%3Ato%5D=40000&search%5Border%5D=created_at%3Adesc#799985302"

current_date: datetime = datetime.now()
formatted_date: str = current_date.strftime('%Y-%m-%d %H:%M:%S')
base: Connection = sqlite3.connect("cars.db")
cur: Cursor = base.cursor()
base.execute("CREATE TABLE IF NOT EXISTS data(link PRIMARY KEY, price, name, data)")
base.commit()


async def show_cars():
    print("started")
    chrome_options: Options = Options()
    chrome_options.add_argument("--headless")

    driver: WebDriver = webdriver.Chrome(options=chrome_options)
    driver.get(olx_url)

    divs: list[WebElement] = driver.find_elements(By.XPATH, "//div[@data-cy='l-card']")

    links: list[WebElement] = driver.find_elements("tag name", "a")

    car_links: list[str | None] = [link.get_attribute("href") for link in links
                                   if link.get_attribute("href").startswith("https://www.olx.ua/d/uk/obyavlenie")]

    names: list[str] = [div.find_element(By.XPATH, ".//h6").text for div in divs]
    prices: list[str] = [div.find_element(By.XPATH, ".//p").text for div in divs]

    query: str = """
    INSERT OR REPLACE INTO data (link, price, name, data)
    VALUES (?, ?, ?, ?)
    """

    update_query: str = """
        UPDATE data
        SET price = ?,
            name = ?
        WHERE link = ?
    """

    for i in range(0, len(car_links)):
        link: str | None = car_links[i]
        price: str = prices[i]
        name: str = names[i]
        cur.execute("SELECT link FROM data WHERE link = ?", (link,))
        existing_record: object = cur.fetchone()
        if existing_record:
            cur.execute(update_query, (price, name, link))
        else:
            cur.execute(query, (link, price, name, formatted_date))
    base.commit()

    driver.quit()
    print("finished")
