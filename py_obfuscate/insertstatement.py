from abc import ABC, abstractmethod

class InsertStatement(ABC):

    # Returns the insert statement
    @abstractmethod
    def to_string(self):
        pass

    @abstractmethod
    def table(self):
        pass

    
    @abstractmethod
    def empty(self):
        pass
    
    # Iterates over inserted rows
    @abstractmethod
    def __iter__(self):
        pass