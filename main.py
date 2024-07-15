# 離散數學
url = "https://ocw.nycu.edu.tw/?course_page=all-course%2Fcollege-of-computer-science%2F%E9%9B%A2%E6%95%A3%E6%95%B8%E5%AD%B8-discrete-mathematics-99%E5%AD%B8%E5%B9%B4%E5%BA%A6-%E8%B3%87%E8%A8%8A%E5%B7%A5%E7%A8%8B%E5%AD%B8%E7%B3%BB-%E6%98%93%E5%BF%97%E5%81%89%E8%80%81%E5%B8%AB"
download_folder = "videos"
target = ".mp4"

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

# disable ssl warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get html content
import requests

response = requests.get(url, headers=headers, verify=False)

html = response.text

# parse html content
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# find all links end with target
import re

links = soup.find_all("a", href=re.compile(target))


# use progressbar to show download progress
from tqdm import tqdm

for link in tqdm(links):
    parent = link.parent
    # find link's parent get class="column-1" and class="column-2"'s text
    column1 = parent.find_previous_sibling("td", class_="column-1")
    column2 = parent.find_previous_sibling("td", class_="column-2")

    title = column1.text + " " + column2.text.split('\n')[0].replace("/",
                                                                     "_")

    # create download folder
    import os

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # download video
    video_url = link["href"]
    video_response = requests.get(video_url, headers=headers, verify=False)
    video = video_response.content

    with open(f"{download_folder}/{title}.mp4", "wb") as f:
        f.write(video)
        print(f"Downloaded {title}.mp4")
