#!/usr/bin/env python3
# encoding: utf-8

# this permits to handle cabanis crappy site

import re
from pathlib import Path
from main import Book
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from icecream import ic
from logzero import logger
from requests_cache import CachedSession
import os
import yaml
from dejapris.isbn import get_book_from_isbn


SESSION_DIR = Path("session")
ACCOUNT_PAGE = SESSION_DIR / "account.html"
BOOK_DETAIL = SESSION_DIR / "book_detail.html"

ROOT_URL = "http://catalogues.toulouse.fr"

SESSION = CachedSession(
    "cabanis_cache", use_cache_dir=True, expire_after=timedelta(days=1)
)

load_dotenv()
CABANIS_ID=os.getenv("CABANIS_ID")
CABANIS_PASSWORD=os.getenv("CABANIS_PASSWORD")

def login() -> requests.Session:
    # session = requests.Session()
    url = ROOT_URL + "/html/Welcome.html"

    # Go to welcome page to get a session number
    url = ROOT_URL + "/web2/tramp2.exe/log_in?setting_key=BMT2"
    logger.info(f"get {url}")
    # first requests must not be cached since 
    response = requests.get(url)
    response.raise_for_status()
    (SESSION_DIR / "00_welcome.html").write_text(response.text)
    # in this page the session token and login url is under
    # <a class="moncompte" href="/web2/tramp2.exe/goto/A12csrum.000?screen=MyAccount.html">
    soup = BeautifulSoup(response.text, features="html.parser")

    login_url = None
    for href in soup.find_all("a"):
        if "class" in href.attrs:
            if href["class"] == ["moncompte"]:
                login_url = href["href"]
                # ic(login_url)
    assert login_url
    url = ROOT_URL + login_url
    response = SESSION.get(url)
    response.raise_for_status()
    (SESSION_DIR / "01_login.html").write_text(response.text)
    # get the FORM action url to know where to send the POST request
    soup = BeautifulSoup(response.text, features="html.parser")

    login_post_url = None
    for item in soup.find_all("form"):
        if item["name"] == "loginWN":
            login_post_url = item["action"]

    assert login_post_url
    url = ROOT_URL + login_post_url
    logger.info(f"LOGIN: POST to {url}")
    payload = {"userid": CABANIS_ID, "pin": CABANIS_PASSWORD, "screen": "MyAccount.html"}
    response = SESSION.post(url, payload)
    response.raise_for_status()

    ACCOUNT_PAGE.write_text(response.text)

BOOK_LINK = "1home&query=(TI"


def parse_prets(account_list: Path = ACCOUNT_PAGE):
    soup = BeautifulSoup(account_list.read_text(), features="html.parser")
    my_books = []
    # Les bouquins en pret sont dans le div id=panel2
    # les resas dans le panel3
    panel2 = soup.find("div", id="panel2")
    assert panel2

    for href in panel2.find_all("a"):
        # ic(href)
        if "href" not in href.attrs:
            continue
        href_link = href.attrs["href"]
        if BOOK_LINK in href_link:
            # ic(href_link)
            my_books.append(href_link)

    if len(my_books) == 0:
        logger.error("no book link found!")
    return my_books


def get_book_from_url(search_url):
    url = ROOT_URL + search_url
    pattern = r".*\(TI ([^)]*)\)"
    book_title = re.match(pattern, search_url).group(1)
    logger.info(f"Download {book_title}: {url}")
    response = SESSION.get(url)
    response.raise_for_status()
    BOOK_DETAIL.write_text(response.text)
    # soup = BeautifulSoup(response.text, features="html.parser")

    # on tombe sur plusieurs exemplaires, Ce site étant de la merde
    # impossible de récupérer plus d'infos...
    # la liste des resultats est clicable, mais avec requests ca ne marche pas
    # bref, tant pis, on ajoutera a la main

    # if soup.find("title") and soup.find("title").text != "Notice Détaillée Web2":
    #     ic("not Notice Détaillée")
        
        # for item in soup.find_all("a"):

        #     if "href" in item.attrs and "see_record" in item.attrs["href"]:
        #         new_url = ROOT_URL + item.attrs["href"]
        #         logger.info(f"Download {book_title}: {url}")
        #         response = SESSION.get(url)
        #         response.raise_for_status()
        #         BOOK_DETAIL.write_text(response.text)
                
        #         break
                

    return book_title

def get_book_isbn_from_page(page: Path) -> Optional[str]:
    soup = BeautifulSoup(page.read_text(), features="html.parser")
    try:
        isbn = soup.find("div", id="isbn_livre").text.strip()
        return isbn
    except AttributeError:
        # no isbn means it is not a book
        # could be a DVD for instance
        # no worries
        return None


def main():
    login()

    my_books = parse_prets()
    mdict = {}
    for book_url in my_books:
        book_title = get_book_from_url(book_url)
        isbn = get_book_isbn_from_page(BOOK_DETAIL)
        mdict[book_title] = isbn

    isbns = []
    for book_title, isbn in mdict.items():
        if isbn:
            print(f"{isbn}: {book_title}")
            isbns.append(isbn)
        else:
            print(f"00000: {book_title}")

    books = []
    print("### ISBNS ###")
    print(isbns)
    for isbn in isbns:

        book = get_book_from_isbn(isbn)
        if book:
            books.append(book)
    print("### YAML ###")
    yaml.dump_all([book.dict() for book in books])

if __name__ == "__main__":
    main()
