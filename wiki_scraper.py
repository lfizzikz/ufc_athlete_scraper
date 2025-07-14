import csv
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

# name = "Dustin_Poirier"
name = "Jiří_Procházka"
url = f"https://en.wikipedia.org/wiki/{name}"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

section = soup.find("h2", id="Mixed_martial_arts_record")

tables = section.find_all_next("table", class_="wikitable", limit=2)
pro_table = tables[1]

headers = [th.get_text(strip=True) for th in pro_table.find_all("tr")[0].find_all("th")]

rows = []
for tr in pro_table.find_all("tr")[1:]:
    cells = tr.find_all(["td", "th"])
    row = [cell.get_text(strip=True) for cell in cells]
    if row:
        rows.append(row)

with open("mma_record.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print("saved")
