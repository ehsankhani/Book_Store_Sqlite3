import sqlite3


def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 year INTEGER NOT NULL)''')

    # Insert some data
    c.execute("INSERT INTO books (title, author, year) VALUES ('1984', 'George Orwell', 1949)")
    c.execute("INSERT INTO books (title, author, year) VALUES ('To Kill a Mockingbird', 'Harper Lee', 1960)")
    c.execute("INSERT INTO books (title, author, year) VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 1925)")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
