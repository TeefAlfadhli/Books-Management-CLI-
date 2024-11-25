
# Book Management CLI Documentation

## Overview
This document provides a detailed explanation of the Book Management CLI script. 
The script enables users to manage a collection of books using commands such as add, update, delete, list, and search.

## Data Storage
Books are stored in a JSON file (`books.json`). Each book record has the following properties:

- **id**: Unique identifier for the book.
- **title**: The title of the book.
- **Author**: The name of the author (note the uppercase `A`).
- **status**: The current status of the book (e.g., Read or Unread).
- **createdAt**: Timestamp when the book was added.
- **updatedAt**: Timestamp when the book was last modified.

## Functions

### 1. `load_books()`
**Purpose**: Loads books from the JSON file. Returns an empty list if the file does not exist.

```python
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    return []
```

### 2. `save_books(books)`
**Purpose**: Saves the current list of books to the JSON file, ensuring data persistence.

```python
def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)
```

### 3. `add_books(title, Author)`
**Purpose**: Adds a new book to the collection. Ensures each book has a unique ID, and stores creation and update timestamps.

**Code:**
```python
def add_books(title, Author):
    books = load_books()
    book_id = max([book["id"] for book in books], default=0) + 1
    book = {
        "id": book_id,
        "title": title,
        "Author": Author,
        "status": "Read",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    books.append(book)
    save_books(books)
    print(f"Book added successfully (ID: {book_id})")
```

### 4. `update_book(book_id, title, status)`
**Purpose**: Updates the title and status of an existing book.

**Code:**
```python
def update_book(book_id, title, status):
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            book["title"] = title
            book["status"] = status
            book["updatedAt"] = datetime.now().isoformat()
            save_books(books)
            print(f"Task {book_id} updated successfully")
            return
    print(f"Task with ID {book_id} not found")
```

### 5. `delete_books(book_id)`
**Purpose**: Deletes a book by its `id`.

**Code:**
```python
def delete_books(book_id):
    books = load_books()
    books = [book for book in books if book["id"] != book_id]
    save_books(books)
    print(f"Book {book_id} deleted successfully")
```

### 6. `list_books(status=None)`
**Purpose**: Lists all books or filters by status.

**Code:**
```python
def list_books(status=None):
    books = load_books()
    if status:
        books = [book for book in books if book["status"] == status]
    if books:
        for book in books:
            print(f"[{book['id']}] {book['title']} (Status: {book['status']})")
    else:
        print("No book found.")
```

### 7. `search_books(title=None, author=None)`
**Purpose**: Searches for books by `title` or `author`.

**Case Sensitivity**: The key `Author` in the JSON is case-sensitive. Ensure you use `Author` instead of `author`.

**Code:**
```python
def search_books(title=None, author=None):
    books = load_books()
    results = []
    for book in books:
        if (title and title.lower() in book["title"].lower()) or            (author and author.lower() in book["Author"].lower()):
            results.append(book)

    if results:
        print("Search Results:")
        for book in results:
            print(f"[{book['id']}] {book['title']} by {book['Author']} (Status: {book['status']})")
    else:
        print("No books found matching the search criteria.")
```

## Commands
Below are the commands supported by the CLI:

- `add`: Add a new book.
- `update`: Update an existing book.
- `delete`: Delete a book by ID.
- `list`: List all books or filter by status.
- `search`: Search for a book by title or author.

## Example Usage
Here are some example commands:

```bash
# Add a new book
python Books-Cli.py add "1984" "George Orwell"

# Update a book
python Books-Cli.py update 1 "Animal Farm" "Unread"

# Delete a book
python Books-Cli.py delete 1

# List all books
python Books-Cli.py list

# Search for a book by title
python Books-Cli.py search --title "1984"

# Search for a book by author
python Books-Cli.py search --author "George Orwell"
```

## Case Sensitivity
- **JSON Keys**: The script uses `Author` (uppercase A) for the author field. Ensure consistency to avoid errors.
- **Search**: The `search_books` function ensures case-insensitive matching for both `title` and `Author`.

