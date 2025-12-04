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


def getTextOfAboutPlease(url):
    resp = requests.get(url).text
    soup = BeautifulSoup(resp, "html.parser")
    about = soup.select_one("#about + p")
    if about is not None:
        return(about.text)
    else:
        about = soup.select_one("#overview + p")
    return about.text
    
max_pages = get_max_page()

with open("thedata/known_memes.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    hrefs = {d["kym_url"] for d in reader}
    


with open("thedata/known_memes.csv", "a", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # writer.writerow(["description", "kym_url", "image_url", "theAbout"]) # if file is new

    
    for page in range(1, max_pages + 1):
        print(f"scraping page {page} of {max_pages}")

        resp = requests.get(
            f"https://knowyourmeme.com/memes/page/{page}?kind=confirmed&sort=newest"
        ).text

        soup = BeautifulSoup(resp, "html.parser")

        for a in soup.select("div.groups a"):
            href = a.attrs.get("href")
            link = f"https://knowyourmeme.com{href}"
            title = a.attrs.get("data-title")
            img = a.select_one("div.not-vertical-only img")
            src = img.attrs.get("src") if img else "n/a"

            if href is not None and title is not None and src is not None:
                if link in hrefs:
                    print(f"67 skipping {link}")
                    pass
                if link not in hrefs:     
                    about = getTextOfAboutPlease(link)
                    print(title, about)
                    writer.writerow((str(title), link, str(src), about))
                    sleep(0.5)
            else:
                raise RuntimeError(f"bad values: {[href, title, src]}\ntag: {a.prettify()}")
            

        sleep(0.5)  # try not to get banned