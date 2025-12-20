from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from database import engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Library Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Add Author
# ---------------------------
@app.post("/authors")
def add_author(name: str):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO authors (name) VALUES (:name)"),
            {"name": name}
        )
        conn.commit()
    return {"message": "Author added successfully"}

# ---------------------------
# Add Book
# ---------------------------
@app.post("/books")
def add_book(title: str, author_id: int, published_year: int):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO books (title, author_id, published_year)
                VALUES (:title, :author_id, :published_year)
            """),
            {
                "title": title,
                "author_id": author_id,
                "published_year": published_year
            }
        )
        conn.commit()
    return {"message": "Book added successfully"}

# ---------------------------
# List Books
# ---------------------------
@app.get("/books")
def list_books():
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT books.id, books.title, authors.name AS author, books.published_year
                FROM books
                JOIN authors ON books.author_id = authors.id
            """)
        )
        books = [dict(row) for row in result.mappings()]
    return books

# ---------------------------
# Update Book
# ---------------------------
@app.put("/books/{book_id}")
def update_book(book_id: int, title: str, published_year: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                UPDATE books
                SET title = :title, published_year = :published_year
                WHERE id = :id
            """),
            {
                "id": book_id,
                "title": title,
                "published_year": published_year
            }
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book updated successfully"}

# ---------------------------
# Delete Book
# ---------------------------
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM books WHERE id = :id"),
            {"id": book_id}
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}
