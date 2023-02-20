from pathlib import Path
from model import Book
from datetime import timedelta

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from icecream import ic
from logzero import logger
from requests_cache import CachedSession
import os
import yaml


SESSION_DIR = Path("session")
ACCOUNT_PAGE = SESSION_DIR / "account.html"
BOOK_DETAIL = SESSION_DIR / "book_detail.html"

SESSION = CachedSession(
    "cabanis_cache", use_cache_dir=True, expire_after=timedelta(days=1)
)

OPENLIB_URL = "http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
def get_book_from_isbn(isbn: str) -> Book:
    # try openlibrary
    # OPENLIB_URL is moisi
    # url = OPENLIB_URL.format(isbn=isbn)
    # response = SESSION.get(url)
    # response.raise_for_status()
    # r_json = response.json()
    # title = None
    # author = None
    # if f"ISBN:{isbn}" in r_json:
        # book = r_json[f"ISBN:{isbn}"]["details"]
        # ic(book)
        # title = book["title"]
        # if "authors" in book:
            # author = book["authors"][0]["name"]
            # return Book(title=title, author=author, isbn=isbn)

    url = 'https://www.babelio.com/recherche.php'
    response = SESSION.post(url, data={"Recherche": isbn})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="html.parser")
    (SESSION_DIR / "isbn.html").write_text(response.text)
    items = soup.find_all("a", class_='titre1')
    if items:
        title = items[0].text
        
        author = soup.find_all("div", class_="sgst_auteur_txt")[0].find("a").text
        return Book(title=title, author=author, isbn=isbn)
    print(f"Faild to find info on isbn ({isbn})")
    return None

