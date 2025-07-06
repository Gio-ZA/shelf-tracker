"""
Book and Author Management System

This program manages a book inventory and author database using SQLite.
Users can:
- Add new books or authors (with ID validation)
- Update book details (quantity, title, or author ID)
- Delete books or authors (with checks for related records)
- Search for books and view all book records

The system ensures that author IDs in books match existing authors and
prevents accidental data loss.
"""
import sqlite3

DB_NAME = "ebookstore.db"


def connect_db() -> sqlite3.Connection:
    """
    Establishes and returns a connection to the SQLite database.

    Returns:
        sqlite3.Connection: The connection object to the database.
    """
    return sqlite3.connect(DB_NAME)


def create_tables(db: sqlite3.Connection) -> None:
    """
    Creates the 'book' and 'author' tables in the database if they do
    not exist.

    Args:
        db (sqlite3.Connection): The active database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    # TEMP CODE: Only use during setup/testing
    # cursor.execute('DROP TABLE IF EXISTS book')
    # cursor.execute('DROP TABLE IF EXISTS author')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            authorID INTEGER,
            qty INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
        )
    ''')

    db.commit()


def insert_sample_data(db: sqlite3.Connection) -> None:
    """
    Inserts sample book and author data into the database.

    Args:
        db (sqlite3.Connection): The active database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    book_data = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)
    ]

    author_data = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")
    ]

    cursor.executemany(
        "INSERT INTO book(id, title, authorID, qty) VALUES (?, ?, ?, ?)",
        book_data
    )
    print("Books added\n")

    cursor.executemany(
        "INSERT INTO author(id, name, country) VALUES (?, ?, ?)",
        author_data
    )
    print("Authors added\n")

    db.commit()


def cancel_operation(user_input: str) -> bool:
    """
    Checks if the user wants to cancel the current input operation.

    If the user enters 'x' (in any case), a cancellation message is
    printed and the function returns True to indicate the process
    should stop.

    Args:
        user_input (str): The input entered by the user.

    Returns:
        bool: True if the user entered 'x' to cancel, otherwise False.
    """
    if user_input.lower() == "x":
        print("Operation cancelled.")
        return True
    return False


def commit_and_print(db: sqlite3.Connection, message: str) -> None:
    """
    Commits changes to the SQLite database and prints a confirmation
    message.

    This utility function ensures that changes made via SQL queries
    are saved permanently and informs the user that the operation was
    successful.

    Args:
        db (sqlite3.Connection): The active SQLite database connection
        to commit.
        message (str): A message to display after committing the
        changes.

    Returns:
        None
    """
    db.commit()
    print(message)


def add_author(db: sqlite3.Connection) -> None:
    """
    Prompts the user to enter and add a new author to the database.

    The function ensures that:
    - The author ID is unique, numeric, and exactly 4 digits
    - The author's name and country are not empty (with feedback)
    - Users can type 'x' at any prompt to cancel the operation

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    while True:
        author_input = input(
            "Enter new 4-digit author ID or 'x' to cancel: "
        ).strip()
        if author_input.lower() == "x":
            print("Operation cancelled.")
            return

        if not author_input.isdigit() or len(author_input) != 4:
            print("Author ID must be a numeric value with exactly 4 digits.\n")
            continue

        author_id = int(author_input)
        cursor.execute("SELECT * FROM author WHERE id = ?", (author_id,))
        if cursor.fetchone():
            print("An author with that ID already exists. Try another.\n")
        else:
            break

    name = input("Enter author name: ").strip().title()
    if not name:
        print("Author name cannot be empty.")
        return

    country = input("Enter author's country: ").strip().title()
    if not country:
        print("Author country cannot be empty.")
        return

    cursor.execute(
        "INSERT INTO author(id, name, country) VALUES (?, ?, ?)",
        (author_id, name, country)
    )
    commit_and_print(db, "Author added successfully.\n")


def add_book_or_author(db: sqlite3.Connection) -> None:
    """
    Prompts the user to choose whether to add a new book or a new
    author.

    If the user selects 'book':
    - Ensures the book ID is unique, numeric, and exactly 4 digits
    - Verifies that the provided author ID exists and is exactly 4
    digits
    - Validates that title is not empty and quantity is a non-negative
    integer
    - Inserts the new book into the 'book' table

    If the user selects 'author':
    - Calls the add_author() function to handle author creation

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    while True:
        choice = input(
            "What would you like to add?"
            " ('Book' or 'Author', or 'x' to cancel): "
        ).strip().lower()
        if cancel_operation(choice):
            return

        if choice == "book":
            cursor = db.cursor()

            # Get a unique 4-digit book ID
            while True:
                book_id_input = input(
                    "Enter 4-digit book ID or 'x' to cancel: "
                    ).strip()
                if cancel_operation(book_id_input):
                    return
                if not book_id_input.isdigit() or len(book_id_input) != 4:
                    print(
                        "Book ID must be a numeric value with exactly 4"
                        " digits.\n"
                    )
                    continue

                book_id = int(book_id_input)
                cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
                if cursor.fetchone():
                    print(
                        "A book with that ID already exists. Please enter a"
                        " different ID.\n"
                    )
                else:
                    break

            # Get the book title
            title = input("Enter book title or 'x' to cancel: ").strip()
            if cancel_operation(title):
                return
            if not title:
                print("Book title is required.\n")
                return

            # Get a valid 4-digit author ID
            while True:
                author_id_input = input(
                    "Enter 4-digit author ID or 'x' to cancel: "
                ).strip()
                if cancel_operation(author_id_input):
                    return
                if not author_id_input.isdigit() or len(author_id_input) != 4:
                    print(
                        "Author ID must be a numeric value with exactly 4"
                        " digits.\n"
                        )
                    continue

                author_id = int(author_id_input)
                cursor.execute("SELECT * FROM author WHERE id = ?",
                               (author_id,))
                if cursor.fetchone():
                    break
                print(
                    "No author found with that ID. Please enter a valid"
                    " author ID.\n"
                )

            # Get quantity
            while True:
                qty_input = input("Enter quantity or 'x' to cancel: ").strip()
                if cancel_operation(qty_input):
                    return
                if not qty_input:
                    print("Quantity is required.\n")
                    continue
                try:
                    qty = int(qty_input)
                    if qty >= 0:
                        break
                    print("Quantity cannot be negative.\n")
                except ValueError:
                    print("Invalid input. Please enter a numeric quantity.\n")

            # Insert the book
            cursor.execute(
                '''
                INSERT INTO book(id, title, authorID, qty)
                VALUES(?, ?, ?, ?)
                ''',
                (book_id, title, author_id, qty)
            )
            commit_and_print(db, "Book added successfully.\n")
            return

        if choice == "author":
            add_author(db)
            return

        print(
            "Invalid input. "
            "Please type 'book', 'author', or 'x' to cancel.\n"
        )


def update_book(db: sqlite3.Connection) -> None:
    """
    Prompts the user to update information for a specific book in the
    database.

    The user selects a book by ID, and can then choose to update one of
    the following:
    - Quantity: Validated as a non-negative integer
    - Title: Cannot be empty
    - Author ID: Must refer to an existing author in the 'author' table
    - Author details: Allows updating the associated author's name and
      country

    All updates are committed to the database if the inputs are valid.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    # Get valid book ID
    while True:
        book_id_input = input(
            "Enter the ID of the book to update (or 'x' to cancel): "
        ).strip()
        if cancel_operation(book_id_input):
            return
        if not book_id_input:
            print("Book ID is required.\n")
            continue

        if not book_id_input.isdigit() or len(book_id_input) != 4:
            print("Book ID must be a 4-digit number.\n")
            continue
        book_id = int(book_id_input)
        cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        if book:
            break

        print("No book found with that ID. Please try again.\n")

    print(
        f"\nCurrent book details:\nID: {book[0]}\nTitle: {book[1]}\n"
        f"AuthorID: {book[2]}\nQuantity: {book[3]}\n"
    )

    # Ask and update field
    while True:
        update_choice = input(
            "What would you like to update?"
            " (qty/title/authorID/author) "
            "[default is qty, 'x' to cancel]: "
        ).strip().lower()
        if cancel_operation(update_choice):
            return
        if update_choice == "":
            update_choice = "qty"

        if update_choice == "qty":
            while True:
                new_qty_input = input(
                    "Enter new quantity (or 'x' to cancel): "
                ).strip()
                if cancel_operation(new_qty_input):
                    return
                if not new_qty_input:
                    print("Quantity is required.\n")
                    continue
                try:
                    new_qty = int(new_qty_input)
                    if new_qty < 0:
                        print("Quantity cannot be negative.\n")
                        continue
                    cursor.execute(
                        "UPDATE book SET qty = ? WHERE id = ?",
                        (new_qty, book_id)
                    )
                    commit_and_print(db, "Quantity updated successfully.\n")
                    return
                except ValueError:
                    print("Invalid quantity. Please enter a number.\n")

        elif update_choice == "title":
            while True:
                new_title = input(
                    "Enter new title (or 'x' to cancel): "
                ).strip()
                if cancel_operation(new_title):
                    return
                if not new_title:
                    print("Title cannot be empty. Please try again.\n")
                    continue
                cursor.execute("UPDATE book SET title = ? WHERE id = ?",
                               (new_title, book_id))
                commit_and_print(db, "Title updated successfully.\n")
                return

        elif update_choice == "authorid":
            while True:
                new_author_id_input = input(
                    "Enter new author ID "
                    "(must already exist, or 'x' to cancel): "
                ).strip()
                if cancel_operation(new_author_id_input):
                    return
                if not new_author_id_input:
                    print("Author ID is required.\n")
                    continue

                if (
                    not new_author_id_input.isdigit() or
                    len(new_author_id_input) != 4
                ):
                    print("Author ID must be a 4-digit number.\n")
                    continue
                new_author_id = int(new_author_id_input)
                cursor.execute("SELECT * FROM author WHERE id = ?",
                               (new_author_id,))
                if cursor.fetchone():
                    cursor.execute(
                        "UPDATE book SET authorID = ? WHERE id = ?",
                        (new_author_id, book_id)
                    )
                    commit_and_print(
                        db, "Book's author ID updated successfully.\n"
                    )
                    return

                print(
                    "The author ID does not exist."
                    " Please enter an existing author ID.\n"
                )

        elif update_choice == "author":
            cursor.execute("SELECT name, country FROM author WHERE id = ?",
                           (book[2],))
            author = cursor.fetchone()

            if author:
                print(f"\nCurrent Author Name: {author[0]}")
                print(f"Current Author Country: {author[1]}\n")

                new_name = input(
                    "Enter new author name (or press Enter to keep current"
                    ", or 'x' to cancel): "
                ).strip()
                if cancel_operation(new_name):
                    return
                new_country = input(
                    "Enter new author country (or press Enter to keep"
                    " current, or 'x' to cancel): "
                ).strip()
                if cancel_operation(new_country):
                    return

                if new_name == "":
                    new_name = author[0]
                if new_country == "":
                    new_country = author[1]

                cursor.execute(
                    "UPDATE author SET name = ?, country = ? WHERE id = ?",
                    (new_name, new_country, book[2])
                )
                commit_and_print(
                    db, "Author information updated successfully.\n"
                )
                return

            print("Author not found for this book.\n")

        else:
            print(
                "Invalid field. Please choose from: qty, title, authorID,"
                " or author.\n"
            )


def delete_author(db: sqlite3.Connection) -> None:
    """
    Deletes an author from the database after validation and
    confirmation.

    Prompts the user for an author ID, ensures the author exists, checks
    if they have any books, and confirms deletion. Cancels the operation
    if the author has books or the user chooses not to proceed.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    while True:
        author_id_input = input(
            "Enter the 4-digit ID of the author to delete (or 'x' to cancel): "
        ).strip()
        if cancel_operation(author_id_input):
            return
        if not author_id_input:
            print("Author ID is required.\n")
            continue
        if not author_id_input.isdigit() or len(author_id_input) != 4:
            print("Author ID must be a 4-digit number.\n")
            continue

        author_id = int(author_id_input)
        cursor.execute("SELECT * FROM author WHERE id = ?", (author_id,))
        author = cursor.fetchone()
        if author:
            break
        print("No author found with that ID. Try again.\n")

    # Check for books by this author
    cursor.execute("SELECT * FROM book WHERE authorID = ?", (author_id,))
    books = cursor.fetchall()
    if books:
        print("This author has books associated with them.")
        print("Please delete those books first.\n")
        return

    # Show author info before deletion
    print(
        f"\nAuthor selected:\nID: {author[0]}\nName: {author[1]}"
        f"\nCountry: {author[2]}\n"
    )

    # Confirm deletion
    while True:
        confirm = input(
            "Delete this author? (yes/no): "
        ).strip().lower()
        if cancel_operation(confirm):
            return
        if confirm == "yes":
            cursor.execute("DELETE FROM author WHERE id = ?", (author_id,))
            commit_and_print(db, "Author deleted successfully.\n")
            return
        if confirm == "no":
            print("Deletion cancelled.\n")
            return

        print("Please type 'yes' or 'no'.")


def delete_book_or_author(db: sqlite3.Connection) -> None:
    """
    Allows the user to delete either a book or an author.

    Prompts the user to choose what to delete. If deleting a book,
    the function validates the book ID, shows details, and confirms
    deletion. If deleting an author, the delete_author() function is
    called. Users can cancel at any prompt by entering 'x'.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    while True:
        choice = input(
            "What would you like to delete? "
            "('Book' or 'Author' or 'x' to cancel): "
        ).strip().lower()
        if cancel_operation(choice):
            return
        if not choice:
            print("Input cannot be blank.\n")
            continue

        if choice == "book":
            while True:
                book_input = input(
                    "Enter the 4-digit ID of the book to delete "
                    "(or 'x' to cancel): "
                ).strip()
                if cancel_operation(book_input):
                    return
                if not book_input:
                    print("Book ID is required.\n")
                    continue
                if not book_input.isdigit() or len(book_input) != 4:
                    print("Book ID must be a 4-digit number.\n")
                    continue

                book_id = int(book_input)
                cursor.execute("SELECT * FROM book WHERE id = ?",
                               (book_id,))
                book = cursor.fetchone()
                if book:
                    break
                print("No book found with that ID.\n")

            # Show book details
            print(
                f"\nBook selected:\nID: {book[0]}\nTitle: {book[1]}"
                f"\nAuthorID: {book[2]}\nQuantity: {book[3]}\n"
            )

            while True:
                confirm = input(
                    "Delete this book? (yes/no): "
                ).strip().lower()
                if confirm == "yes":
                    cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
                    commit_and_print(db, "Book deleted successfully.\n")
                    return
                if confirm == "no":
                    print("Deletion cancelled.\n")
                    return

                print("Please type 'yes' or 'no'.\n")

        elif choice == "author":
            delete_author(db)
            return
        else:
            print("Invalid option. Choose 'Book' or 'Author'.\n")


def search_books(db: sqlite3.Connection) -> None:
    """
    Allows the user to search for books by ID or title.

    The user can choose to search by book ID or by a partial/full title.
    - When searching by ID, the function validates the input and shows
      the matching book details if found.
    - When searching by title, it performs a partial match and lists all
      matching books.

    The user can cancel the search at any prompt by entering 'x'.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    cursor = db.cursor()

    while True:
        search_by = input(
            "Search by ID or title? "
            "(type 'id' or 'title', or 'x' to cancel): "
        ).strip().lower()

        if cancel_operation(search_by):
            return
        if not search_by:
            print("Input cannot be blank.\n")
            continue

        if search_by == "id":
            book_input = input(
                "Enter the 4-digit book ID (or 'x' to cancel): "
            ).strip()
            if cancel_operation(book_input):
                return
            if not book_input:
                print("Book ID is required.\n")
                continue
            if not book_input.isdigit() or len(book_input) != 4:
                print("Book ID must be a 4-digit number.\n")
                continue

            book_id = int(book_input)
            cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if book:
                print(
                    f"\nBook found:\nID: {book[0]}\nTitle: {book[1]}"
                    f"\nAuthorID: {book[2]}\nQuantity: {book[3]}\n"
                )
                return

            print("No book found with that ID.\n")

        elif search_by == "title":
            title = input(
                "Enter the book title (or part of it, or 'x' to cancel): "
            ).strip()
            if cancel_operation(title):
                return
            if not title:
                print("Book title is required.\n")
                continue
            cursor.execute("SELECT * FROM book WHERE title LIKE ?",
                           (f'%{title}%',))
            books = cursor.fetchall()
            if books:
                print("\nBooks found:")
                for book in books:
                    print(
                        f"ID: {book[0]} | Title: {book[1]} | AuthorID: "
                        f"{book[2]} | Quantity: {book[3]}"
                    )
                print()
                return

            print("No books found matching that title.\n")

        else:
            print("Invalid option. Please type 'id', 'title', or 'x'.\n")


def view_all_books(db: sqlite3.Connection) -> None:
    """
    Displays detailed information for all books along with their
    authors.

    Retrieves and prints the title of each book, the corresponding
    author's name, and the author's country in a formatted layout.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    print("\nDetails")
    print("-" * 55)

    cursor = db.cursor()

    cursor.execute(
        '''
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author ON book.authorID = author.id
        '''
    )

    results = cursor.fetchall()

    for title, name, country in results:
        print(f"Title: {title}")
        print(f"Author's Name: {name}")
        print(f"Author's Country: {country}")
        print("-" * 55)


def main_menu(db: sqlite3.Connection) -> None:
    """
    Displays the main menu, prompts the user for options,
    and calls appropriate functions to manage the book and author
    database.

    Args:
        db (sqlite3.Connection): An active SQLite database connection.

    Returns:
        None
    """
    while True:
        menu = input(
            '''Select one of the following options:
    1 - add book/author
    2 - update book
    3 - delete book/author
    4 - search books
    5 - view details of all books
    0 - exit
    : '''
        ).strip()

        if menu == "1":
            add_book_or_author(db)
        elif menu == "2":
            update_book(db)
        elif menu == "3":
            delete_book_or_author(db)
        elif menu == "4":
            search_books(db)
        elif menu == "5":
            view_all_books(db)
        elif menu == "0":
            print('Goodbye!!!')
            break
        else:
            print("Invalid option.")


with connect_db() as db:
    create_tables(db)
    insert_sample_data(db)

    main_menu(db)
