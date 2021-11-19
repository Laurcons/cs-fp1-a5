from random import *

from src.domain.book import Book, BookValidator
from src.repository.repository import Repository

class NotUniqueException(Exception):
    pass

class BookService:
    def __init__(self, repository: Repository):
        self.__repo = repository

    def populate(self):
        """ Adds 10 random books. """
        for i in range(0, 10):
            # generate an ISBN
            isbn = "ISBN xxx-xxx-xxx-xxx-"
            digit_sum = 0
            digit_idx = 0
            for x in range(0, len(isbn)):
                if isbn[x] != 'x': continue
                digit = randrange(0, 10)
                isbn = isbn[:x] + str(digit) + isbn[x+1:]
                digit_sum += digit * (3 if digit_idx % 2 == 1 else 1)
                digit_idx += 1
            check = 10 - (digit_sum % 10)
            check = check if check != 10 else 0
            isbn += str(check)
            # keep a fixed author and title
            self.add_book(isbn, "UBB", "Why UBB is the Best University in the World", with_transaction=False)

    def add_book(self, isbn, author, title, with_transaction=True):
        """ Adds a book.
        """
        book = Book(isbn, author, title)
        if self.__repo.has_id(book.isbn_unique):
            raise NotUniqueException("The book ISBN is not unique!")
        self.__repo.insert(book, with_transaction=with_transaction)

    def get_all_books(self):
        """ Returns all books.
        """
        return self.__repo.get_all()

    def filter_by_word(self, word):
        """ Removes all books from the database whose titles start with the given word.
        :param word: The word to remove books by.
        :return: The number of books that have been deleted.
        """
        pred = lambda bk: bk.title.lower().startswith(word.lower() + ' ')
        # to_delete = self.__repo.find_all_by_predicate(pred)
        # if len(to_delete) > 0:
        #     self.__repo.start_undoable_transaction()
        # count = 0
        # for bk in to_delete:
        #     count += 1
        #     self.__repo.remove_id(bk.isbn_unique)
        count = self.__repo.remove_by_predicate(pred)
        return count

    def undo(self):
        """ Undoes the last operation. """
        self.__repo.undo()

def test_book_service():
    repo = Repository("isbn_unique", BookValidator)
    svc = BookService(repo)
    try:
        # fail due to invalid ISBN
        svc.add_book("123", "test1", "test1")
        assert(False)
    except: pass

    # success
    svc.add_book("1234567890128", "916", "How To Anger Gabi")

    try:
        # fail due to not unique ISBN
        svc.add_book("ISBN 123-456-789-012-8", "917", "How To Anger Gabi")
        assert(False)
    except: pass

    # success
    assert svc.filter_by_word("how") == 1
    assert len(svc.get_all_books()) == 0


test_book_service()