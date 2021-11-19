import traceback

from src.domain.book import ValidationException
from src.repository.history import NothingToUndoException
from src.services.book_service import BookService, NotUniqueException

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Console:
    """ Provides an interface between services and the Human. """

    def __init__(self, book_service: BookService):
        self.__book_service = book_service
        self.__options = {
            1: self.option_add_book,
            2: self.option_display_all_books,
            3: self.option_filter_by_word,
            4: self.option_undo,
        }

    def __print_error(self, text):
        print(Colors.FAIL + text + Colors.ENDC)

    def __print_success(self, text):
        print(Colors.OKGREEN + text + Colors.ENDC)

    def __print_warning(self, text):
        print(Colors.WARNING + text + Colors.ENDC)

    def __print_menu(self):
        print(Colors.OKBLUE +
              "Welcome to The Amazing Book Manager (TABM)! What do you want to do?\n"
              "1. Add a book\n"
              "2. Display all the books\n"
              "3. Filter (remove) list by word\n"
              "4. Undo\n"
              "x. Exit" + Colors.ENDC)

    def option_add_book(self):
        print("Let's add a book together! I firstly need some information.")
        isbn = input("What's the ISBN code? ").strip()
        author = input("What's the author? ").strip()
        title = input("What's the title? ").strip()
        print("Thanks! I'm now trying to add the book...")
        try:
            self.__book_service.add_book(isbn, author, title)
            self.__print_success("Thanks! The book has been added.")
        except NotUniqueException:
            self.__print_error("Couldn't add your book! The ISBN code is not unique.")
        except ValidationException as e:
            self.__print_error(f"Couldn't add your book! The ISBN is invalid. {e}")
        except Exception as e:
            self.__print_error(f"Couldn't add your book! {e}")

    def option_display_all_books(self):
        print(Colors.BOLD + "Displaying all books now..." + Colors.ENDC)
        books = self.__book_service.get_all_books()
        for book in books:
            print(book)
        if len(books) > 0:
            print("These are all the books.")
        else:
            self.__print_error("There are no books! Go add some.")

    def option_filter_by_word(self):
        print("Let's filter some books together! I firstly need some information.")
        word = input("What word do you want to filter by? ").strip()
        print("I'm filtering now...")
        try:
            count = self.__book_service.filter_by_word(word)
        except Exception as e:
            self.__print_error(f"Something happened. {e}")
        if count == 0:
            self.__print_warning("Nothing was deleted. Are you sure you typed the right word?")
        else: self.__print_success(f"A number of {count} books were deleted.")

    def option_undo(self):
        print("I'm now undoing...")
        try:
            self.__book_service.undo()
            self.__print_success("Successfully undone last action!")
        except NothingToUndoException:
            self.__print_error("There was nothing to undo.")

    def start(self):
        self.__book_service.populate()
        while True:
            self.__print_menu()
            opt = input("Choose an option: ")
            if opt == 'x':
                break
            if not opt.isdigit():
                continue
            opt = int(opt)
            if opt in self.__options:
                try:
                    self.__options[opt]()
                except Exception as e:
                    self.__print_error(f"Something HORRIBLE has happened! Please investigate! {e}")
                    print(traceback.print_tb(e.__traceback__))
            else:
                self.__print_error("Option unknown!")
