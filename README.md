# 📚 Book and Author Management System

A Python application that manages a book inventory and author database using SQLite. This system allows users to add, update, search, and delete book and author records with built-in validation to prevent data inconsistencies and accidental data loss.

---

## 🚀 Features

- ➕ Add new books or authors  
- ✏️ Update book details (quantity, title, or author ID)  
- ❌ Delete books or authors (with safeguards to prevent deleting authors linked to books)  
- 🔍 Search for books by title or ID  
- 📋 View all book records in the database  
- ✅ Validates that all book author IDs exist in the author table

---

## 🗃️ Sample Data (Auto-loaded on Setup)

**Books**  
| Book ID | Title                                    | Author ID | Quantity |
|---------|------------------------------------------|-----------|----------|
| 3001    | A Tale of Two Cities                     | 1290      | 30       |
| 3002    | Harry Potter and the Philosopher's Stone | 8937      | 40       |
| 3003    | The Lion, the Witch and the Wardrobe     | 2356      | 25       |
| 3004    | The Lord of the Rings                    | 6380      | 37       |
| 3005    | Alice's Adventures in Wonderland         | 5620      | 12       |

**Authors**  
| Author ID | Name             | Country        |
|-----------|------------------|----------------|
| 1290      | Charles Dickens  | England        |
| 8937      | J.K. Rowling     | England        |
| 2356      | C.S. Lewis       | Ireland        |
| 6380      | J.R.R. Tolkien   | South Africa   |
| 5620      | Lewis Carroll    | England        |

---

## 📁 Files Included

- `shelf_track.py` — Main Python script
- `ebookstore.db` — SQLite database (created automatically if not present)

---

## 🔧 How to Run

1. Make sure Python 3 is installed
2. Clone or download this repository
3. Run the program:
   ```bash
   python book_author_manager.py

---

🛠️ Technologies Used

Python 3

SQLite (sqlite3 module)

File-based local database

---

📌 Notes

Author IDs must exist before assigning them to a book

Authors cannot be deleted if they are linked to a book

Uses input validation to ensure clean and consistent data

---

📄 License
This project is open-source and available under the MIT License
