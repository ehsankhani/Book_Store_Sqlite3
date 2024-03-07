import tkinter as tk
from tkinter import messagebox
import sqlite3
from DataBase import create_database


class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        # Call create_database function from database.py to ensure the database exists
        create_database()

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label_title = tk.Label(self.frame, text="Library Management System", font=('Helvetica', 18, 'bold'))
        self.label_title.grid(row=0, column=0, columnspan=3, pady=10)

        self.button_show_books = tk.Button(self.frame, text="Show Books", command=self.show_books)
        self.button_show_books.grid(row=1, column=0, pady=5)

        self.button_add_book = tk.Button(self.frame, text="Add Book", command=self.add_book)
        self.button_add_book.grid(row=1, column=1, pady=5)

        self.button_delete_book = tk.Button(self.frame, text="Delete Book", command=self.delete_book)
        self.button_delete_book.grid(row=1, column=2, pady=5)

        self.button_edit_book = tk.Button(self.frame, text="Edit Book", command=self.edit_book)
        self.button_edit_book.grid(row=2, column=0, pady=5)

        self.button_search_book = tk.Button(self.frame, text="Search Book", command=self.search_book)
        self.button_search_book.grid(row=2, column=1, pady=5)

        self.button_exit = tk.Button(self.frame, text="Exit", command=root.destroy)
        self.button_exit.grid(row=2, column=2, pady=5)

    def show_books(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        conn.close()

        if books:
            book_list = "\n".join([f"Title: {book[1]}, Author: {book[2]}, Year: {book[3]}" for book in books])
            messagebox.showinfo("Books", book_list)
        else:
            messagebox.showinfo("Books", "No books available.")

    def add_book(self):
        # Create a new window for adding a book
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")

        # Labels and entry fields for book details
        tk.Label(add_window, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(add_window)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Author:").grid(row=1, column=0, padx=10, pady=5)
        author_entry = tk.Entry(add_window)
        author_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Year:").grid(row=2, column=0, padx=10, pady=5)
        year_entry = tk.Entry(add_window)
        year_entry.grid(row=2, column=1, padx=10, pady=5)

        # Function to handle adding the book to the database
        def add_to_database():
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()

            # Validation: Ensure all fields are filled
            if title and author and year:
                try:
                    year = int(year)
                    conn = sqlite3.connect('library.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Book added successfully.")
                    add_window.destroy()  # Close the add book window
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid year.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        # Button to confirm adding the book
        add_button = tk.Button(add_window, text="Add Book", command=add_to_database)
        add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def delete_book(self):
        pass

    def edit_book(self):
        pass

    def search_book(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
