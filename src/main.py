from src.domain.book import BookValidator
from src.repository.repository import Repository
from src.services.book_service import BookService
from src.ui.console import Console

repo = Repository("isbn_unique", BookValidator)

book_service = BookService(repo)

console = Console(book_service)

console.start()
