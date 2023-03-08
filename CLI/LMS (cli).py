# library management system

class Member:
    def __init__(self, name, phone, email, book_borrowed=[]):
        self.name = name
        self.phone = phone
        self.email = email
        self.borrowed_books = book_borrowed

    def book_borrow(self, book):
        self.borrowed_books.append(book)

    def book_return(self, book):
        self.borrowed_books.remove(book)

    def show_details(self):
        print(f"{self.name}\n{self.phone}\n{self.email}\n{self.borrowed_books}\n")


class Book:
    def __init__(self, title, author, subject, publication):
        self.title = title
        self.author = author
        self.subject = subject
        self.publication = publication

    def show_details(self):
        print(f"{self.title}\n{self.author}\n{self.subject}\n{self.publication}\n")


class RecordHandler:
    @staticmethod
    def save_members():
        f = open("members.txt", "w+")
        for member in members_list:
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
        f = open(f"books.txt", "w+")
        for book in book_list:
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

    def remove_book(self, title):
        for book in self.book_list:
            if book.title == title:
                self.book_list.remove(book)

    def search_book(self, category, search_text):  # might give error because or category thing
        d = {"title": "book.title", "author": "book.author", "subject": "book.subject",
             "publication": "book.publication"}
        x = False
        for book in self.book_list:
            if search_text in eval(d.get(category)):
                book.show_details()
                x = True
        return x

    def display_all_books(self):
        for book in self.book_list:
            book.show_details()


class DataBank:
    def __init__(self, members):
        self.members_list = members

    def add_member(self, name, phone, email):
        self.members_list.append(Member(name, phone, email))

    def remove_member(self, name):
        for member in self.members_list:
            if member.name == name:
                self.members_list.remove(member)

    def search_member(self, name):
        for member in self.members_list:
            if member.name == name:
                member.show_details()
                return member
        print(" no such member exist / wrong member name entered")

    def display_all_members(self):
        for member in self.members_list:
            member.show_details()


# driver code
# initialization

members_list = []
book_list = []
R1 = RecordHandler()
R1.load_members()
R1.load_books()
bookshelf = BookShelf(book_list)
data_bank = DataBank(members_list)

# _______________________________________


while True:
    print("""
                            <========== LIBRARY MANAGEMENT SYSTEM ===========>
                                   
                            1) CHECK OUT BOOK
                            2) RETURN A BOOK
                            3) RESERVE A BOOK
                            4) RE BORROW A BOOK
                            5) MEMBERS DATA
                            6) ADD / REMOVE A BOOK 
                            7) EXIT
                            
                             
    """)

    choice = input("enter your choice ==> ")
    if choice == "1":
        bookshelf.display_all_books()
        print("""
                            1) SHOW ALL BOOKS
                            2) SEARCH A BOOK
                            3) BORROW A BOOK
                            4) BACK (<--)
    """)
        while True:
            choice = input("enter your choice ==> ")
            if choice == "1":
                bookshelf.sort_books()
                bookshelf.display_all_books()
                break

            if choice == "2":
                search_by = input("search by ? ( title,author,subject,publication )==> ")
                n = input("search for ==> ")
                if bookshelf.search_book(search_by, n):
                    break
                print(f" no results found for {n} in {search_by} ")

            elif choice == "3":
                n = input("enter member name ==> ")
                m = data_bank.search_member(n)
                b = input("enter book name ==> ")
                if bookshelf.search_book("title", b):
                    m.book_borrow(b)
                    break
                print(f" book {n} is not available in our library right now")

            elif choice == "4":
                break

    elif choice == "2":
        n = input("enter member name ==> ")
        m = data_bank.search_member(n)
        b = input("enter book name ==> ")
        if bookshelf.search_book("title", b):
            m.book_return(b)
        print(f" book {n} is not available in our library right now")

    elif choice == "3":
        n = input("enter member name ==> ")
        m = data_bank.search_member(n)
        bk = input("enter book name ==> ")
        print(f"book {bk} has been reserved for {n} ")

    elif choice == "4":
        n = input("enter member name ==> ")
        m = data_bank.search_member(n)
        b = input("enter book name ==> ")
        if n in m.borrowed_books:
            print(f" the book {n} has been re borrowed by {n}  ")
        else:
            print("book has not been borrowed earlier")

    elif choice == "5":
        print("""
                1) SEARCH MEMBER
                2) REGISTER NEW ACCOUNT
                3) REMOVE ACCOUNT
                4) BACK (<--)
        """)
        while True:
            choice = input("enter your choice ==> ")
            if choice == "1":
                n = input("enter member name ==> ")
                m = data_bank.search_member(n)

            elif choice == "2":
                n = input("enter member name ==> ")
                p = input("enter member phone number ==> ")
                e = input("enter member email ==> ")
                data_bank.add_member(n, p, e)

            elif choice == "3":
                n = input("enter member name ==> ")
                data_bank.remove_member(n)

            elif choice == "4":
                break

    elif choice == "6":
        print("""
                        1) ADD A BOOK
                        2) REMOVE A BOOK 
                        3) BACK (<--)

        """)
        while True:
            choice = input("enter your choice ==> ")
            if choice == "1":
                t = input("enter book title ==> ")
                a = input("enter author name ==> ")
                s = input("enter book subject ==> ")
                p = input("enter book publication ==> ")
                bookshelf.add_book(t, a, s, p)

            elif choice == "2":
                t = input("enter book title ==> ")
                bookshelf.remove_book(t)
            elif choice == "3":
                break

    elif choice == "7":
        R1.save_books()
        R1.save_members()
        print("program exited")
        break
