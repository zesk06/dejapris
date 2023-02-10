from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


books = [
    {"title": "GamingGame", "isbn": "12345", "dejapris": True},
    {"title": "Squid life", "isbn": "54321", "dejapris": False},
]


class Book(BaseModel):
    title: str
    isbn: str
    dejapris: bool


class Message(BaseModel):
    detail: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/book/{isbn}",
    response_model=Book,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"title": "bar", "isbn": "12345", "dejapris": True}
                }
            },
        },
    },
)
async def get_book_by_isbn(isbn):
    for book in books:
        if book["isbn"] == isbn:
            return Book(**book)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book not found (isbn={isbn})")
