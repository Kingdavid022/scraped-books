import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

session = requests.Session()
session.headers.update(HEADERS)

def get_soup(url):
    """Return BeautifulSoup object of a webpage."""
    res = session.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def main():
    page = 1
    image_links = []

    while True:
        if page == 1:
            url = BASE_URL
        else:
            url = urljoin(BASE_URL, f"catalogue/page-{page}.html")

        soup = get_soup(url)
        books = soup.select("article.product_pod")

        if not books:
            break  # No more pages

        for book in books:
            rel_link = book.select_one("h3 a")["href"]
            book_url = urljoin(url, rel_link)

            # Go inside the book details page
            book_soup = get_soup(book_url)
            img_tag = book_soup.select_one("div.thumbnail img")

            if img_tag:
                img_src = urljoin(book_url, img_tag["src"])
                image_links.append(img_src)
                print(img_src)  #  Print each image link exactly like your example

        page += 1

    # Optional: Save to text file
    with open("image_links.txt", "w", encoding="utf-8") as f:
        for link in image_links:
            f.write(link + "\n")

if __name__ == "__main__":
    main()
