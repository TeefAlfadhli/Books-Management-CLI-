import argparse
import json
import os
from datetime import datetime

# File to store tasks
BOOKS_FILE = "books.json"

# Load tasks from the JSON file
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to the JSON file
def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)


# Add a new task
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


# Update an existing task
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


# Delete a task
def delete_books(book_id):
    books = load_books()
    books = [book for book in books if book["id"] != book_id]
    save_books(books)
    print(f"Book {book_id} deleted successfully")


# List tasks
def list_books(status=None):
    books = load_books()
    if status:
        books = [book for book in books if book["status"] == status]
    if books:
        for book in books:
            print(f"[{book['id']}] {book['title']} (Status: {book['status']})")
    else:
        print("No book found.")

# Search For A Book
def search_books(title=None, author=None):
    books = load_books()
    results = []

    # Ensure case-insensitive comparison for both title and author
    for book in books:
        if (title and title.lower() in book["title"].lower()) or \
           (author and author.lower() in book["Author"].lower()):  # Use "Author" with uppercase "A"
            results.append(book)

    # Display results or show 'No books found'
    if results:
        print("Search Results:")
        for book in results:
            print(f"[{book['id']}] {book['title']} by {book['Author']} (Status: {book['status']})")
    else:
        print("No books found matching the search criteria.")




# Argument parser setup
parser = argparse.ArgumentParser(description="Book Management CLI")
subparsers = parser.add_subparsers(dest="command", help="Commands")

# Add subcommand
add_parser = subparsers.add_parser("add", help="Add a new book")
add_parser.add_argument("title", type=str, help="Title of the book")
add_parser.add_argument("Author", type=str, help="Author of the book")


# Update subcommand
update_parser = subparsers.add_parser("update", help="Update an existing task")
update_parser.add_argument("id", type=int, help="ID of the Book to update")
update_parser.add_argument("title", type=str, help="New Title of the Book")
update_parser.add_argument("status", type=str, help="New status of the book")

# Delete subcommand
delete_parser = subparsers.add_parser("delete", help="Delete a Book")
delete_parser.add_argument("id", type=int, help="ID of the book to delete")


# List subcommand
list_parser = subparsers.add_parser("list", help="List tasks")
list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter tasks by status")

# Add search subcommand
search_parser = subparsers.add_parser("search", help="Search for a book")
search_parser.add_argument("--title", type=str, help="Search by book title")
search_parser.add_argument("--author", type=str, help="Search by book author")

# Parse arguments
args = parser.parse_args()

# Handle commands
if args.command == "add":
    add_books(args.title, args.Author)
elif args.command == "update":
    update_book(args.id, args.title, args.status)
elif args.command == "delete":
    delete_books(args.id)
elif args.command == "list":
    list_books(args.status)
elif args.command == "search":
    search_books(title=args.title, author=args.author)
else:
    parser.print_help()
