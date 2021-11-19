
class NothingToUndoException(Exception):
    pass

class History:
    """ Provides methods to manage snapshots of a datastore, along with undo and redo operations
    """
    def __init__(self):
        self.__snapshots = []

    def push(self, datastore):
        """ Pushes a snapshot of the datastore """
        self.__snapshots.append(dict(datastore))

    def undo(self, datastore: dict):
        """ Retrieves a snapshot from the history and assigns it to the datastore """
        if len(self.__snapshots) == 0:
            raise NothingToUndoException()
        datastore.clear()
        datastore.update(self.__snapshots.pop())

def test_history():
    hist = History()
    datastore = {}
    hist.push(datastore)
    datastore['4'] = 13

    hist.push(datastore)
    datastore['2'] = 16

    hist.undo(datastore)
    assert(len(datastore) == 1)

test_history()