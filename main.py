import csv
import time
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

page = 0
fighters = []
seen = set()

while True:
    url = f"https://www.ufc.com/athletes/all?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    fighter_cards = soup.find_all("li", class_="l-flex__item")

    if not fighter_cards:
        break

    added_this_page = 0

    for card in fighter_cards:
        name_tag = card.find("span", class_="c-listing-athlete__name")
        record_tag = card.find("span", class_="c-listing-athlete__record")
        weight_tag = card.find(
            "div",
            class_="field field--name-stats-weight-class field--type-entity-reference field--label-hidden field__items",
        )
        nick_name_tag = card.find(
            "span",
            class_="c-listing-athlete__nickname",
        )

        name = name_tag.text.strip() if name_tag else "N/A"
        record = record_tag.text.strip() if name_tag else "N/A"
        weight_class = weight_tag.text.strip() if weight_tag else "N/A"
        nick_name = nick_name_tag.text.strip() if nick_name_tag else "N/A"

        if name in seen:
            continue
        seen.add(name)
        fighters.append(
            {
                "name": name,
                "record": record,
                "weight_class": weight_class,
                "nick_name": nick_name,
            }
        )
        added_this_page += 1

    print(f"{added_this_page} fighters added from page {page}")
    page += 1
    time.sleep(1)

with open("fighters.csv", "a", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["name", "record", "weight_class", "nick_name"]
    )
    writer.writeheader()
    writer.writerows(fighters)
