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
        # Fetch books from the database
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        conn.close()

        if not books:
            messagebox.showinfo("Delete Book", "No books available to delete.")
            return

        # Create a new window for deleting a book
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Book")

        # Display the list of books with corresponding IDs
        tk.Label(delete_window, text="Select a book to delete:").grid(row=0, column=0, padx=10, pady=5)
        book_listbox = tk.Listbox(delete_window, width=50, height=10)
        book_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        for book in books:
            book_listbox.insert(tk.END, f"{book[0]}. {book[1]} by {book[2]} ({book[3]})")

        # Function to handle deleting the selected book
        def delete_from_database():
            selected_book_index = book_listbox.curselection()
            if selected_book_index:
                book_id = books[selected_book_index[0]][0]
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute("DELETE FROM books WHERE id=?", (book_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Book deleted successfully.")
                delete_window.destroy()  # Close the delete book window
            else:
                messagebox.showerror("Error", "Please select a book to delete.")

        # Button to confirm deleting the selected book
        delete_button = tk.Button(delete_window, text="Delete Book", command=delete_from_database)
        delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def edit_book(self):
        # Fetch books from the database
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        conn.close()

        if not books:
            messagebox.showinfo("Edit Book", "No books available to edit.")
            return

        # Create a new window for editing a book
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Book")

        # Display the list of books with corresponding IDs
        tk.Label(edit_window, text="Select a book to edit:").grid(row=0, column=0, padx=10, pady=5)
        book_listbox = tk.Listbox(edit_window, width=50, height=10)
        book_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        for book in books:
            book_listbox.insert(tk.END, f"{book[0]}. {book[1]} by {book[2]} ({book[3]})")

        # Function to handle selecting a book for editing
        def select_book_for_edit():
            selected_book_index = book_listbox.curselection()
            if selected_book_index:
                book_id = books[selected_book_index[0]][0]
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute("SELECT * FROM books WHERE id=?", (book_id,))
                book = c.fetchone()
                conn.close()
                show_edit_options(book)
            else:
                messagebox.showerror("Error", "Please select a book to edit.")

        # Button to confirm selecting a book for editing
        select_button = tk.Button(edit_window, text="Select Book", command=select_book_for_edit)
        select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        def show_edit_options(book):
            # Create a new window to show edit options
            edit_options_window = tk.Toplevel(edit_window)
            edit_options_window.title("Edit Book")

            # Display the parameters that can be edited for the selected book
            tk.Label(edit_options_window, text="Edit Options:").grid(row=0, column=0, padx=10, pady=5)
            edit_options_listbox = tk.Listbox(edit_options_window, width=50, height=10)
            edit_options_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

            edit_options_listbox.insert(tk.END, "Title")
            edit_options_listbox.insert(tk.END, "Author")
            edit_options_listbox.insert(tk.END, "Year")

            # Function to handle editing the selected book
            def edit_selected_option():
                selected_option_index = edit_options_listbox.curselection()
                if selected_option_index:
                    selected_option = edit_options_listbox.get(selected_option_index)
                    edit_value(selected_option, book)
                else:
                    messagebox.showerror("Error", "Please select an option to edit.")

            # Button to confirm selecting an option for editing
            select_option_button = tk.Button(edit_options_window, text="Select Option", command=edit_selected_option)
            select_option_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        def edit_value(option, book):
            # Create a new window to edit the value
            edit_value_window = tk.Toplevel(edit_window)
            edit_value_window.title("Edit Value")

            tk.Label(edit_value_window, text=f"Enter new {option}:").grid(row=0, column=0, padx=10, pady=5)
            value_entry = tk.Entry(edit_value_window)
            value_entry.grid(row=0, column=1, padx=10, pady=5)

            # Function to handle updating the book value in the database
            def update_book_value():
                new_value = value_entry.get()
                if new_value:
                    try:
                        if option == "Year":
                            new_value = int(new_value)
                        conn = sqlite3.connect('library.db')
                        c = conn.cursor()
                        c.execute(f"UPDATE books SET {option.lower()}=? WHERE id=?", (new_value, book[0]))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Book details updated successfully.")
                        edit_value_window.destroy()
                        edit_window.destroy()
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid year.")
                else:
                    messagebox.showerror("Error", "Please enter a value.")

            update_button = tk.Button(edit_value_window, text="Update", command=update_book_value)
            update_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def search_book(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
