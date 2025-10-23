"""
Scrapes knowyourmeme.com for a summary of all confirmed memes.
Outputs a csv with (description, knowyourmeme.com detail url, image url)
"""

import csv
from time import sleep
import requests
from bs4 import BeautifulSoup


def get_max_page():
    page_nums: list[int] = []
    page_0 = requests.get(
        f"https://knowyourmeme.com/memes?kind=confirmed&sort=newest"
    ).text
    soup = BeautifulSoup(page_0, "html.parser")

    page_buttons = soup.select("a.page-button")

    for pb in page_buttons:
        try:
            page_nums.append(int(pb.text))
        except:
            pass

    return max(page_nums)


rows: list[tuple[str, str, str]] = []
max_pages = get_max_page()
for page in range(1, max_pages + 1):
    print(f"scraping page {page} of {max_pages}")

    resp = requests.get(
        f"https://knowyourmeme.com/memes/page/{page}?kind=confirmed&sort=newest"
    ).text

    soup = BeautifulSoup(resp, "html.parser")

    for a in soup.select("div.groups a"):
        href = a.attrs.get("href")
        alt = a.attrs.get("alt")
        img = a.select_one("div.not-vertical-only img")
        src = img.attrs.get("src") if img else "n/a"

        if href is not None and alt is not None and src is not None:
            rows.append((str(alt), f"https://knowyourmeme.com{href}", str(src)))
        else:
            raise RuntimeError(f"bad values: {[href, alt, src]}\ntag: {a.prettify()}")

    sleep(0.5)  # try not to get banned

with open("known_memes.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["description", "kym_url", "image_url"])
    writer.writerows(rows)

print(f"scraped {len(rows)} memes")
