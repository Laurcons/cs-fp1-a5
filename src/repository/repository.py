from src.domain.book import BookValidator, Book
from src.repository.history import History


class EntityNotFoundException(Exception):
    pass

class Repository:
    def __init__(self, id_name: str, validator):
        self.__entities = {}
        self.__history = History()
        self.__id_name = id_name
        self.__validator = validator

    def start_undoable_transaction(self):
        self.__history.push(self.__entities)

    def undo(self):
        self.__history.undo(self.__entities)

    def insert(self, entity, with_transaction=True):
        """ Adds or overwrites the entity (using the Id as a primary key).
        :return: Nothing
        """
        if with_transaction:
            self.__history.push(self.__entities)
        self.__validator.validate(entity)
        self.__entities[getattr(entity, self.__id_name)] = entity

    def has_id(self, id):
        """ Returns true if the specified id already exists.
        :param id: The id
        :return: True or False, as specified
        """
        return id in self.__entities

    def find_by_id(self, id):
        """ Finds the entity with the given id. If not found, throw EntityNotFoundException
        :return: The entity
        """
        if id not in self.__entities:
            raise EntityNotFoundException()
        return self.__entities[id]

    def find_all_by_predicate(self, predicate):
        """ Finds all entities that satisfy the given predicate.
        :param predicate: A function that takes an entity and returns True or False.
        :return: A list of entities, or an empty list.
        """
        return [ent for ent in self.__entities.values() if predicate(ent)]

    def find_by_predicate(self, predicate):
        """ Finds one entity that satisfies the given predicate.
        :param predicate: A function that takes an entity and returns True or False.
        :return: The found predicate, or None if nothing was found.
        """
        for ent in self.__entities.values():
            if predicate(ent):
                return ent
        return None

    def remove_id(self, id):
        """ Removes the entity with the given id. If not found, throw EntityNotFoundException
        :return: The removed entity
        """
        if id not in self.__entities:
            raise EntityNotFoundException()
        self.__history.push(self.__entities)
        return self.__entities.pop(id)

    def remove_by_predicate(self, predicate):
        """ Removes all entities that satisfy the given predicate.
        :param predicate: A function that takes an entity and returns True or False.
        :return: The number of deleted entities.
        """
        self.__history.push(self.__entities)
        pre_count = len(self.__entities)
        self.__entities = dict([ent for ent in self.__entities.items() if not predicate(ent[1])])
        post_count = len(self.__entities)
        return pre_count - post_count

    def count(self):
        """ Returns the count of all entities """
        return len(self.__entities)

    def get_all(self):
        """ Returns a list with all the entities.
        """
        return list(self.__entities.values())


def test_repository():
    repo = Repository("isbn_unique", BookValidator)

    repo.insert(Book("123456-7890-12-8", "Hello", "World!"))
    # will replace
    repo.insert(Book("123456-7890-128", "Hello", "World!!!"))
    assert(repo.count() == 1)

    # valid
    repo.insert(Book("9876543210-128", "World", "Bow to me!"))

    # fail validation
    try:
        repo.insert(Book("123-456-7890-123", "This will", "fail!"))
        assert(False)
    except: pass

    # remove an id
    repo.remove_id("9876543210128")
    assert(repo.count() == 1)

    # remove with a predicate that matches against nothing
    repo.remove_by_predicate(lambda bk: bk.title.startswith("Nothing"))
    assert(repo.count() == 1)

test_repository()