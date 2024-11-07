import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from datetime import datetime

class Book:
    def __init__(self, title, author, price, quantity):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} by {self.author}, ${self.price:.2f}, Qty: {self.quantity}"

class BookStore:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, price, quantity):
        book = Book(title, author, price, quantity)
        self.books.append(book)

    def delete_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                return True
        return False

    def edit_book(self, old_title, new_title, author, price, quantity):
        for book in self.books:
            if book.title.lower() == old_title.lower():
                book.title = new_title
                book.author = author
                book.price = price
                book.quantity = quantity
                return True
        return False

    def sell_book(self, title, quantity):
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.quantity >= quantity:
                    book.quantity -= quantity
                    return book.price * quantity  # Return the total sales amount
                else:
                    raise ValueError("Insufficient stock")
        raise ValueError("Book not found")

    def get_books(self):
        return self.books

    def save_books(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Author", "Price", "Quantity"])
            for book in self.books:
                writer.writerow([book.title, book.author, book.price, book.quantity])

    def load_books(self, filename):
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row['Title']
                    author = row['Author']
                    price = float(row['Price'])
                    quantity = int(row['Quantity'])
                    self.books.append(Book(title, author, price, quantity))
        except FileNotFoundError:
            pass

class BookStoreApp:
    def __init__(self, root):
        self.bookstore = BookStore()
        self.bookstore.load_books("books.csv")

        self.root = root
        self.root.title("Book Store Management")
        self.root.geometry("600x500")

        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Book Store Management", font=("Helvetica", 18, "bold")).pack(pady=20)

        tk.Button(self.root, text="Add Book", command=self.show_add_book, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="View Books", command=self.show_view_books, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="Edit Book", command=self.show_edit_book, bg="#FFC107", fg="white").pack(pady=10)
        tk.Button(self.root, text="Delete Book", command=self.show_delete_book, bg="#F44336", fg="white").pack(pady=10)
        tk.Button(self.root, text="Sell Book", command=self.show_sell_book, bg="#009688", fg="white").pack(pady=10)
        tk.Button(self.root, text="Generate Sales Report", command=self.generate_sales_report, bg="#795548", fg="white").pack(pady=10)
        tk.Button(self.root, text="Save Books", command=self.save_books, bg="#9C27B0", fg="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, bg="#607D8B", fg="white").pack(pady=10)

    def show_add_book(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Add a Book", font=("Helvetica", 16)).pack(pady=10)

        self.title_entry = self.create_label_and_entry("Title:")
        self.author_entry = self.create_label_and_entry("Author:")
        self.price_entry = self.create_label_and_entry("Price:")
        self.quantity_entry = self.create_label_and_entry("Quantity:")

        tk.Button(self.root, text="Add Book", command=self.add_book, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.create_main_menu, bg="#607D8B", fg="white").pack(pady=5)

    def create_label_and_entry(self, label_text):
        frame = tk.Frame(self.root)
        frame.pack(pady=2)
        tk.Label(frame, text=label_text, width=20, anchor="w").pack(side="left")
        entry = tk.Entry(frame, width=40)
        entry.pack(side="left")
        return entry

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()

        if title and author and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                if price < 0 or quantity < 0:
                    raise ValueError("Negative value")

                self.bookstore.add_book(title, author, price, quantity)
                self.clear_entries()
                messagebox.showinfo("Success", f"Book '{title}' added successfully.")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid positive values for price and quantity.")
        else:
            messagebox.showerror("Missing Information", "Please fill out all fields.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def show_view_books(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Current Books", font=("Helvetica", 16)).pack(pady=10)

        self.book_list = tk.Listbox(self.root, width=80, height=15)
        self.book_list.pack(pady=10)

        self.view_books()

        tk.Button(self.root, text="Back to Menu", command=self.create_main_menu, bg="#607D8B", fg="white").pack(pady=5)

    def view_books(self):
        self.book_list.delete(0, tk.END)
        books = self.bookstore.get_books()
        if books:
            for book in books:
                self.book_list.insert(tk.END, str(book))
        else:
            self.book_list.insert(tk.END, "No books available.")

    def show_sell_book(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sell a Book", font=("Helvetica", 16)).pack(pady=10)

        self.book_list = tk.Listbox(self.root, width=80, height=15)
        self.book_list.pack(pady=10)

        self.view_books()

        self.quantity_entry = self.create_label_and_entry("Quantity to Sell:")

        tk.Button(self.root, text="Sell Selected Book", command=self.sell_book, bg="#009688", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.create_main_menu, bg="#607D8B", fg="white").pack(pady=5)

    def sell_book(self):
        selected_item = self.book_list.get(tk.ACTIVE)
        if selected_item:
            title = selected_item.split(" by ")[0]
            quantity = self.quantity_entry.get()
            if quantity.isdigit():
                quantity = int(quantity)
                try:
                    total_price = self.bookstore.sell_book(title, quantity)
                    self.log_sale(title, quantity, total_price)
                    messagebox.showinfo("Success", f"Sold {quantity} copies of '{title}' for ${total_price:.2f}")
                    self.view_books()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid quantity.")
        else:
            messagebox.showerror("No Selection", "Please select a book to sell.")

    def log_sale(self, title, quantity, total_price):
        with open("sales_report.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, quantity, total_price])

    def generate_sales_report(self):
        try:
            with open("sales_report.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                report = "\n".join([", ".join(row) for row in reader])

            report_window = tk.Toplevel(self.root)
            report_window.title("Sales Report")
            report_window.geometry("500x400")
            tk.Label(report_window, text="Sales Report", font=("Helvetica", 16, "bold")).pack(pady=10)
            report_text = tk.Text(report_window, wrap="word")
            report_text.insert("1.0", report)
            report_text.pack(expand=True, fill="both")
        except FileNotFoundError:
            messagebox.showerror("Error", "No sales report available.")

    def save_books(self):
        self.bookstore.save_books("books.csv")
        messagebox.showinfo("Success", "Books saved to 'books.csv' successfully.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BookStoreApp(root)
    root.mainloop()
