# library management system
import tkinter
from tkinter import *


class Member:
    def __init__(self, name, phone, email, book_borrowed=[]):
        self.name = name
        self.phone = phone
        self.email = email
        self.borrowed_books = book_borrowed

    def book_borrow(self, book):
        self.borrowed_books.append(book)
        R1.save_members()

    def book_return(self, book):
        self.borrowed_books.remove(book)
        R1.save_members()

    def show_details(self):
        return f"NAME: {self.name} \nPHONE: {self.phone}\nEMAIL: {self.email}\nBORROWED BOOKS: {self.borrowed_books}\n\n"


class Book:
    def __init__(self, title, author, subject, publication):
        self.title = title
        self.author = author
        self.subject = subject
        self.publication = publication

    def show_details(self):
        return (
            f"TITLE: {self.title} \nAUTHOR: {self.author} \nSUBJECT: {self.subject} \nPUBLICATION: {self.publication}\n\n")


class RecordHandler:
    @staticmethod
    def save_members():
        f = open("members.txt", "w+")
        for member in data_bank.members_list:
            f.write(f"{member.name}|{member.phone}|{member.email}|{member.borrowed_books}\n")
        f.close()

    @staticmethod
    def load_members():
        try:
            f = open(f"members.txt", "r+")
            records = f.read().split("\n")
            records.pop()
            n = True
        except FileNotFoundError:
            records = []
            n = False
        for record in records:
            info = record.split("|")
            member = Member(info[0], info[1], info[2], eval(info[3]))
            members_list.append(member)
        if n:
            f.close()

    @staticmethod
    def save_books():
        bookshelf.sort_books()
        f = open(f"books.txt", "w+")
        for book in bookshelf.book_list:
            f.write(f"{book.title}|{book.author}|{book.subject}|{book.publication}\n")
        f.close()

    @staticmethod
    def load_books():
        try:
            f = open(f"books.txt", "r+")
            records = f.read().split("\n")
            records.pop()
            n = True
        except FileNotFoundError:
            records = []
            n = False
        for record in records:
            info = record.split("|")
            book = Book(info[0], info[1], info[2], info[3])
            book_list.append(book)
        if n:
            f.close()


class BookShelf:
    def __init__(self, books):
        self.book_list = books

    # implementation of Quick sort algorithm to sort books by title
    def sort_books(self):
        def swap(one, two):
            temp = self.book_list[one]
            self.book_list[one] = self.book_list[two]
            self.book_list[two] = temp

        def quicksort(start, end):
            if start >= end: return
            partition_idx = partition(start, end)
            quicksort(start, partition_idx - 1)
            quicksort(partition_idx + 1, end)

        def partition(start, end):
            pivot = self.book_list[end]
            partition_idx = start
            for i in range(start, end):
                if self.book_list[i].title <= pivot.title:
                    swap(i, partition_idx)
                    partition_idx += 1
            swap(partition_idx, end)
            return partition_idx

        quicksort(0, len(self.book_list) - 1)

    def add_book(self, title, author, subject, publication):
        book = Book(title, author, subject, publication)
        self.book_list.append(book)
        self.sort_books()
        R1.save_books()

    def remove_book(self, title):
        for book in self.book_list:
            if book.title == title:
                self.book_list.remove(book)
                R1.save_books()
                return
        t1.delete("1.0", "end")
        t1.insert(INSERT, f" THIS BOOK IS NOT AVAILABLE ")

    def search_book(self, category, search_text):
        d = {"title": "book.title", "author": "book.author", "subject": "book.subject",
             "publication": "book.publication"}
        x = False
        t1.delete("1.0", "end")
        for book in self.book_list:
            if search_text in eval((d.get(category)).lower()):
                t1.insert(INSERT, book.show_details()
                          )
                x = True
        if not x:
            t1.insert(INSERT, " no results found")
        return x

    def reserve_book(self, member, book):
        x = data_bank.search_member(member)
        t1.delete("1.0", "end")
        if x:
            t1.insert(INSERT, f"book '{book}' has been reserved for member '{member}'")
            return
        t1.insert(INSERT, f" MEMBER DOESN'T EXIST ")

    def return_book(self, member, book):
        x = data_bank.search_member(member)
        t1.delete("1.0", "end")
        if x:
            if book in x.borrowed_books:
                t1.insert(INSERT, f"book '{book}' has been returned by member '{member}'")
                x.book_return(book)
                return
            t1.insert(INSERT, f" BOOK NOT BORROWED EARLIER ")
            return
        t1.insert(INSERT, f" MEMBER DOESN'T EXIST ")

    def borrow_book(self, member, book):
        y = self.search_book("title", book)
        x = data_bank.search_member(member)
        t1.delete("1.0", "end")
        if x:
            if y:
                x.book_borrow(book)
                t1.insert(INSERT, f" book '{book}' borrowed by member '{member}' ")
            t1.insert(INSERT, f" THIS BOOK IS NOT AVAILABLE ")
            return
        t1.insert(INSERT, f" MEMBER DOESN'T EXIST ")

    def display_all_books(self):
        t1.delete("1.0", "end")
        count = 1
        for i in self.book_list:
            t1.insert(INSERT, f"BOOK NUMBER # {count}---------------------\n")
            t1.insert(INSERT, i.show_details())
            count += 1


class DataBank:
    def __init__(self, members):
        self.members_list = members

    def add_member(self, name, phone, email):
        t1.delete("1.0", "end")
        self.members_list.append(Member(name, phone, email))
        R1.save_members()
        t1.insert(INSERT, f" new member '{name}' is added to list ")

    def remove_member(self, name):
        t1.delete("1.0", "end")
        for member in self.members_list:
            if member.name == name:
                self.members_list.remove(member)
                R1.save_members()
                t1.insert(INSERT, f" member {name} has been successfully removed from the list ")
                return
        t1.insert(INSERT, f" MEMBER DOESN'T EXIST ")

    def search_member(self, name):
        t1.delete("1.0", "end")
        for member in self.members_list:
            if member.name == name:
                t1.insert(INSERT, member.show_details())
                return member
        t1.insert(INSERT, " no such member exist / wrong member name entered")

    def display_all_members(self):
        count = 1
        t1.delete("1.0", "end")
        for member in self.members_list:
            t1.insert(INSERT, f"BOOK NUMBER # {count}---------------------\n")
            t1.insert(INSERT, member.show_details())
            count += 1


# todo mini shelf screen
def add_book_screen(master):
    f1 = Frame(master, bg="#170311")
    f1.place(relx=0.36, rely=0.05, relheight=0.9, relwidth=0.6)

    l1 = Label(f1, text="TITLE", fg="white", bg="#170311")
    l1.place(relx=0.1, rely=0.05, relheight=0.07, relwidth=0.8)
    e1 = Entry(f1, bg="#F4FF95", fg="#170311")
    e1.place(relx=0.1, rely=0.15, relheight=0.07, relwidth=0.8)

    l2 = Label(f1, text="AUTHOR", fg="white", bg="#170311")
    l2.place(relx=0.1, rely=0.25, relheight=0.07, relwidth=0.8)
    e2 = Entry(f1, bg="#F4FF95", fg="#170311")
    e2.place(relx=0.1, rely=0.35, relheight=0.07, relwidth=0.8)

    l3 = Label(f1, text="SUBJECT", fg="white", bg="#170311")
    l3.place(relx=0.1, rely=0.45, relheight=0.07, relwidth=0.8)
    e3 = Entry(f1, bg="#F4FF95", fg="#170311")
    e3.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

    l4 = Label(f1, text="PUBLICATION", fg="white", bg="#170311")
    l4.place(relx=0.1, rely=0.65, relheight=0.07, relwidth=0.8)
    e4 = Entry(f1, bg="#F4FF95", fg="#170311")
    e4.place(relx=0.1, rely=0.75, relheight=0.07, relwidth=0.8)

    b1 = Button(f1, text="ADD", bg="#624801", fg="white",
                command=lambda: bookshelf.add_book(e1.get(), e2.get(), e3.get(), e4.get()))
    b1.place(relx=0.1, rely=0.85, relheight=0.07, relwidth=0.4)


def mini_shelf_screen(master, p1, p2, p3):
    f1 = Frame(master, bg="#170311")
    f1.place(relx=0.36, rely=0.05, relheight=0.9, relwidth=0.6)

    l1 = Label(f1, text=p1, fg="white", bg="#170311")
    l1.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)
    e1 = Entry(f1, bg="#F4FF95", fg="#170311")
    e1.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.8)

    l2 = Label(f1, text=p2, fg="white", bg="#170311")
    l2.place(relx=0.1, rely=0.35, relheight=0.1, relwidth=0.8)
    e2 = Entry(f1, bg="#F4FF95", fg="#170311")
    e2.place(relx=0.1, rely=0.5, relheight=0.1, relwidth=0.8)

    b1 = Button(f1, text=p3, bg="#624801", fg="white",
                command=lambda: eval(f"bookshelf.{p3.lower()}_book('{e1.get()}','{e2.get()}')"))
    b1.place(relx=0.1, rely=0.65, relheight=0.1, relwidth=0.4)

    # def search


# todo shelf_screen
def shelf_screen():
    shelf_frame = Frame(menu_screen, bg="#F9BD04")
    shelf_frame.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

    show = Button(shelf_frame, text="ALL BOOKS", bg="#624801", fg="white", command=bookshelf.display_all_books)
    show.place(relx=0.02, rely=0.05, relheight=0.1, relwidth=0.3)

    search = Button(shelf_frame, text="SEARCH BOOK", bg="#624801", fg="white",
                    command=lambda: mini_shelf_screen(shelf_frame, "SEARCH CATEGORY", "SEARCH TEXT", "SEARCH"))
    search.place(relx=0.02, rely=0.17, relheight=0.1, relwidth=0.3)

    borrow = Button(shelf_frame, text="BORROW BOOK", bg="#624801", fg="white",
                    command=lambda: mini_shelf_screen(shelf_frame, "MEMBER NAME", "BOOK NAME ", "BORROW"))
    borrow.place(relx=0.02, rely=0.29, relheight=0.1, relwidth=0.3)

    return_book = Button(shelf_frame, text="RETURN BOOK", bg="#624801", fg="white",
                         command=lambda: mini_shelf_screen(shelf_frame, "MEMBER NAME", "BOOK NAME ", "RETURN"))
    return_book.place(relx=0.02, rely=0.41, relheight=0.1, relwidth=0.3)

    reserve = Button(shelf_frame, text="RESERVE BOOK", bg="#624801", fg="white",
                     command=lambda: mini_shelf_screen(shelf_frame, "MEMBER NAME", "BOOK NAME ", "RESERVE"))
    reserve.place(relx=0.02, rely=0.53, relheight=0.1, relwidth=0.3)

    remove = Button(shelf_frame, text="REMOVE BOOK", bg="#624801", fg="white",
                    command=lambda: search_remove_screen(shelf_frame, "BOOK NAME", "REMOVE"))
    remove.place(relx=0.02, rely=0.65, relheight=0.1, relwidth=0.3)

    add = Button(shelf_frame, text="ADD BOOK", bg="#624801", fg="white", command=lambda: add_book_screen(shelf_frame))
    add.place(relx=0.02, rely=0.77, relheight=0.1, relwidth=0.3)


# todo mini member screen
def search_remove_screen(master, p1, p2):
    f1 = Frame(master, bg="#170311")
    f1.place(relx=0.36, rely=0.05, relheight=0.9, relwidth=0.6)

    l1 = Label(f1, text=p1, fg="white", bg="#170311")
    l1.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)
    e1 = Entry(f1, bg="#F4FF95", fg="#170311")
    e1.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.8)

    if p1 == "BOOK NAME":
        b1 = Button(f1, text=p2, bg="#624801", fg="white", command=lambda: eval(f"bookshelf.remove_book('{e1.get()}')"))
    elif p1 == "MEMBER NAME":
        b1 = Button(f1, text=p2, bg="#624801", fg="white",
                    command=lambda: eval(f"data_bank.{p2.lower()}_member('{e1.get()}')"))

    b1.place(relx=0.1, rely=0.35, relheight=0.1, relwidth=0.4)

    # todo add member screen


def add_member_screen(master):
    f1 = Frame(master, bg="#170311")
    f1.place(relx=0.36, rely=0.05, relheight=0.9, relwidth=0.6)

    l1 = Label(f1, text="NAME", fg="white", bg="#170311")
    l1.place(relx=0.1, rely=0.05, relheight=0.07, relwidth=0.8)
    e1 = Entry(f1, bg="#F4FF95", fg="#170311")
    e1.place(relx=0.1, rely=0.15, relheight=0.07, relwidth=0.8)

    l2 = Label(f1, text="PHONE NUMBER", fg="white", bg="#170311")
    l2.place(relx=0.1, rely=0.25, relheight=0.07, relwidth=0.8)
    e2 = Entry(f1, bg="#F4FF95", fg="#170311")
    e2.place(relx=0.1, rely=0.35, relheight=0.07, relwidth=0.8)

    l3 = Label(f1, text="EMAIL", fg="white", bg="#170311")
    l3.place(relx=0.1, rely=0.45, relheight=0.07, relwidth=0.8)
    e3 = Entry(f1, bg="#F4FF95", fg="#170311")
    e3.place(relx=0.1, rely=0.55, relheight=0.07, relwidth=0.8)

    b1 = Button(f1, text="ADD", bg="#624801", fg="white", command=lambda: data_bank.add_member(e1.get(), e2.get(), e3.get()))
    b1.place(relx=0.1, rely=0.85, relheight=0.07, relwidth=0.4)


# todo membership screen
def member_screen():
    member_frame = Frame(menu_screen, bg="#F9BD04")
    member_frame.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

    show = Button(member_frame, text="ALL MEMBERS", bg="#624801", fg="white", command=data_bank.display_all_members)
    show.place(relx=0.02, rely=0.05, relheight=0.1, relwidth=0.3)

    search = Button(member_frame, text="SEARCH MEMBER", bg="#624801", fg="white",
                    command=lambda: search_remove_screen(member_frame, "MEMBER NAME", "SEARCH"))
    search.place(relx=0.02, rely=0.17, relheight=0.1, relwidth=0.3)

    add = Button(member_frame, text="ADD ACCOUNT", bg="#624801", fg="white",
                 command=lambda: add_member_screen(member_frame))

    add.place(relx=0.02, rely=0.29, relheight=0.1, relwidth=0.3)

    remove = Button(member_frame, text="REMOVE ACCOUNT", bg="#624801", fg="white",
                    command=lambda: search_remove_screen(member_frame, "MEMBER NAME", "REMOVE"))
    remove.place(relx=0.02, rely=0.41, relheight=0.1, relwidth=0.3)


# driver code
# initialization

members_list = []
book_list = []
R1 = RecordHandler()
R1.load_members()
R1.load_books()
bookshelf = BookShelf(book_list)
bookshelf.sort_books()
R1.save_books()
data_bank = DataBank(members_list)

root = Tk(className="Library management system")
root.config(background="#170311")
root.minsize(height=500, width=800)
# root.resizable(False, False)

# todo header
header = Label(root, text="LIBRARY MANAGEMENT SYSTEM", font=("times", 20, "bold"), bg="#170311", fg="white")
header.place(relx=0.025, rely=0.02, relheight=0.11, relwidth=0.95)

# todo text screen
text_screen = Frame(root)
text_screen.place(relx=0.525, rely=0.15, relheight=0.8, relwidth=0.45)
s1 = Scrollbar(text_screen)
s1.pack(side=RIGHT, fill=Y)
s2 = Scrollbar(text_screen, orient="horizontal")
s2.pack(side=BOTTOM, fill=X)
t1 = Text(text_screen, bg="#F4FF95", fg="#170311", yscrollcommand=s1.set, xscrollcommand=s2.set, width=100, wrap=NONE)
t1.pack(side=LEFT, fill=X)
s1.config(command=t1.yview)
s2.config(command=t1.xview)

# todo menu_screen
menu_screen = Frame(root, bg="#F9BD04")
menu_screen.place(relx=0.025, rely=0.15, relheight=0.8, relwidth=0.45)
shelf = Button(menu_screen, text="BOOK SHELF", bg="#624801", fg="white", command=shelf_screen)
shelf.place(relx=0, rely=0, relheight=0.1, relwidth=0.5)
memberships = Button(menu_screen, text="MEMBERSHIPS", bg="#624801", fg="white", command=member_screen)
memberships.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.5)

root.mainloop()
