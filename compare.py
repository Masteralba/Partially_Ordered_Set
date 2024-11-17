from abc import *

class Compare_Operarion(ABC):
    @abstractmethod
    def comparable(self):
        pass

    @abstractmethod
    def compare(self):
        pass


class Devide_Comparation(Compare_Operarion):
    
    def __init__(self, x, y):
        if ( not isinstance(x, int) or not isinstance(y, int)): raise ValueError
        self.x = x
        self.y = y

    def comparable(self):
        return ( ( self.y % self.x == 0) or ( self.x % self.y == 0) )
    
    def compare(self):
        return (self.y % self.x == 0)
    


class Comparator:

    def __init__(self, Comparation):
        self.Comparation = Comparation

    def second_is_greater(self, x, y):
        if self.Comparation(x, y).comparable():
            return self.Comparation(x, y).compare()
    
    def equal(self, x, y):
        if self.Comparation(x, y).comparable(): 
            return self.Comparation(y, x).compare() and self.Comparation(x, y).compare()

