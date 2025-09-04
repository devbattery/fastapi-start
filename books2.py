from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  # range(1 to 5)


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingWithRoby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingWithRoby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingWithRoby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]


@app.get("/api/books")
async def read_all_books():
    return BOOKS


@app.post("/api/books/create")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)
    return BOOKS


@app.post("/api/books/create-valid")
async def create_book_valid(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book
