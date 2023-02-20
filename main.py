from typing import List
from typing import Optional
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yaml
from isbn import get_book_from_isbn
from model import Book

app = FastAPI()
app.mount("/site", StaticFiles(directory="site", html=True), name="site")

MAX_NOTE=5

BOOKS_FILE=Path("books.yml")

def load_books(book_path: Path=BOOKS_FILE) -> list[Book]:
    yaml_str = book_path.read_text()
    book_list = yaml.safe_load_all(yaml_str)
    return [Book(**item) for item in book_list]

def save_books(books: List[Book], book_path: Path=BOOKS_FILE):
    yaml_str = yaml.safe_dump_all([book.dict() for book in books])
    book_path.write_text(yaml_str, "utf-8")

class Message(BaseModel):
    detail: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/book/")
async def get_books() -> List[Book]:
    """get all books"""
    return load_books()


@app.post(
    "/book/{isbn}/note/dec",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The book was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
)
async def dec_book_note(isbn) -> Optional[Book]:
    """dec change a book note"""
    books = load_books()
    for book in books:
        if book.isbn == isbn:
            book.note = max(book.note-1, 0)
            save_books(books)
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})"
    )

@app.post(
    "/book/{isbn}/note/inc",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The book was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
)
async def inc_book_note(isbn) -> Optional[Book]:
    """inc change a book note"""
    books = load_books()
    for book in books:
        if book.isbn == isbn:
            book.note = min(book.note+1, MAX_NOTE)
            save_books(books)
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})"
    )

@app.get(
    "/book/{isbn}",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
)
async def get_book_by_isbn(isbn) -> Optional[Book]:
    """get a book by its isbn"""
    for book in load_books():
        if book.isbn == isbn:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})"
    )

@app.post(
    "/book",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        201: {
            "description": "Item created by ID",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
)
async def post_book(book: Book) -> Optional[Book]:
    """Create a new book"""
    books = load_books()

    if book.isbn in [item.isbn for item in books]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book isbn already in database (isbn={book.isbn})"
        )

    books.append(book)
    save_books(books)
    return book

@app.get(
    "/isbn/{isbn}",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "The book detail",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
    status_code=status.HTTP_200_OK
)
async def get_isbn(isbn: str) -> Book:
    """Get a book detail from its isbn, no necessarly in DB"""
    isbn = isbn.replace("-", "")

    book = get_book_from_isbn(isbn)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})"
    )

@app.post(
    "/isbn/{isbn}",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        201: {
            "description": "Item created by ID",
            "content": {
                "application/json": {
                    "example": {
                        "title": "bar",
                        "isbn": "12345",
                        "author": "John Doe",
                        "dejapris": True,
                        "note": 0,
                    }
                }
            },
        },
    },
    status_code=status.HTTP_201_CREATED
)
async def post_isbn(isbn: str) -> Book:
    """Adds a new book to collection from its isbn"""
    isbn = isbn.replace("-", "")
    books = load_books()

    if isbn in [item.isbn for item in books]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"book isbn already in database (isbn={isbn})"
        )

    book = get_book_from_isbn(isbn)
    if book:
        await post_book(book)
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})"
    )
