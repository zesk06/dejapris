from pydantic import BaseModel

class Book(BaseModel):
    author: str
    dejapris: bool=True
    isbn: str
    note: int=0
    title: str

