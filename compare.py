from abc import *

class Compare_Operarion(ABC):
    @classmethod
    @abstractmethod
    def are_comparable(self, x, y):
        pass

    @abstractmethod
    def comapre(self, x, y):
        pass


class Devide_Comparation(Compare_Operarion):
    def are_comparable(self, x, y):
        if ( not isinstance(x, int) or not isinstance(y, int)): raise ValueError
        return ( ( y % x == 0) or ( x % y == 0) )
    


class Compartor:

    def second_is_greater(x, y, Comparation):
        pass
    
    def equal(x, y):
        return ((x % y) == 0 and (y % x) == 0)
    
A = Devide_Comparation
A.are_comparable(5, 6)