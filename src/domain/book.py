import re

class Book:
    def __init__(self, isbn, author, title):
        self.__isbn = isbn
        self.__author = author
        self.__title = title

    @property
    def isbn(self):
        return self.__isbn

    @property
    def isbn_unique(self):
        # return the ISBN without any dashes or other Human tomfuckery
        return self.isbn_to_unique(self.isbn)

    @staticmethod
    def isbn_to_unique(isbn):
        """ Strips all non-digit characters, making the ISBN code verifiably unique
        """
        return ''.join([c for c in isbn if c.isdigit()])

    @property
    def author(self):
        return self.__author

    @property
    def title(self):
        return self.__title

    def __str__(self):
        return f"{self.isbn} / Authored by {self.author} / {self.title}"

    def __repr__(self):
        return f"{{ {self.isbn} / {self.author} / {self.title} }}"

class ValidationException(Exception):
    pass

class BookValidator:
    @staticmethod
    def validate(book):
        # validate ISBN
        isbn_re = re.compile("(ISBN ?)?([0-9]-?){13}")
        match = isbn_re.match(book.isbn)
        if not match:
            raise ValidationException("ISBN format is not accepted or invalid")
        # validate check digit
        # https://en.wikipedia.org/wiki/International_Standard_Book_Number
        digits = []
        for char in book.isbn:
            if char.isdigit():
                digits.append(int(char))
        sum = 0
        for i in range(0, len(digits)):
            sum += digits[i] * (3 if i % 2 == 1 else 1)
        if not sum % 10 == 0:
            proper = 10 - ((sum - digits[12]) % 10)
            proper = proper if proper != 10 else 0
            raise ValidationException(f"ISBN check digit in {book.isbn} is invalid, it should be {proper}")

def test_books():
    try:
        book = Book("1234567890123", "test1", "test1")
        # fail due to invalid check
        BookValidator.validate(book)
        assert(False)
    except:
        pass

    try:
        book = Book("1234567890128", "test1", "test1")
        # pass
        BookValidator.validate(book)
    except:
        assert(False)

    try:
        book = Book("ISBN 12345--67890123", "test1", "test1")
        # invalidly formatted
        BookValidator.validate(book)
        assert(False)
    except:
        pass

test_books()