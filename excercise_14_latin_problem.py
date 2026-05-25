"""
“Tres fratres erant qui singulas sorores habebant, et fluvium transire debebant (erat enim unicuique illorum concupiscientia in sorore proximi sui), qui venientes ad fluvium non invenerunt nisi parvam naviculam, in qua non potuerunt amplius nisi duo ex illis transire. Dicat, qui potest, qualiter fluvium transierunt, ne una quidem earum ex ipsis maculata sit?”
"""

"""
“There were three brothers who each had one sister, and they had to cross a river (for each of them desired the sister of the one next to him).
When they came to the river, they found only a small boat, in which no more than two of them could cross at a time.
Let him say, who can, how they crossed the river so that not even one of the sisters was dishonored?”
"""

"""
- tre coppie fratelli/sorelle
- barca con due posti per attraversare il fiume
- combinazioni che devono essere valide su lato A, lato B e barca sempre
- possono essere solo uomini assieme
- possono essere solo femmine assieme
- possono essere una coppia fratello/sorella piu' ogni altra combinazione
- tutte le altre cobinazioni sono proibite

traduci in un grafo
"""

"""
first, how do I represent a solution? I use a vector where each index is a meaning, and the index is their location

vector:
ma, mb, mc, fa, fb, fc

position:
0, 1, 2 

I need a function that given a solution will tell me if the solution is allowed

each node is a solution

an arc is changing the index

load on boat 0->1 of up to two person

unload from boat 1->2 of up to two person

I don't have other operators

"""

from typing import List

from dataclasses import dataclass, field

from enum import IntEnum

from itertools import product

class E_agent(IntEnum):
    MA = 0
    MB = 1
    MC = 2
    FA = 3
    FB = 4
    FC = 5

class E_location(IntEnum):
    START = 0
    BOAT = 1
    GOAL = 2

    def __repr__(self):
        return str(self.value)

@dataclass
class St_solution:
    ln_location: List[int] = field(default_factory=lambda: [ E_location.START, E_location.START, E_location.START, E_location.START, E_location.START, E_location.START ])

    def __post_init__(self):
        if len(self.ln_location) != 6:
            raise ValueError("Vector must contain exactly 6 positions")

        for n_index in self.ln_location:
            if n_index not in (0, 1, 2):
                raise ValueError("Each position must be 0, 1, or 2")

    def copy(self) -> "St_solution":
        return St_solution(
            ln_location=self.ln_location.copy()
        )

    def get(self, i_e_agent: E_agent) -> int:
        return self.ln_location[i_e_agent]

    def set(self, i_e_agent: E_agent, i_n_value: int) -> None:
        if ln_location not in (0, 1, 2):
            raise ValueError("Value must be 0, 1, or 2")
        self.ln_location[i_e_agent] = i_n_value

    def get_num_location(self, i_e_location : E_location ) -> int:
        return sum(1 for n_location in self.ln_location if n_location == i_e_location)

    def is_invalid(self)->bool:
        """
        [0,0,0,0,0,0] is valid. each female has their associated male
        [1,0,0,1,0,0] is valid. MA is with FA on BOAT
        [1,1,0,1,0,0] is invalid. three on the boat at one time
        [1,0,0,0,1,0] is invalid. MA is with FB on BOAT
        [2,0,0,0,2,0] is invalid. MA is with FB on GOAL
        [0,0,0,2,2,2] is valid. female on goal have no opposite male with them

        It's invalid if there are three on boat
        It's valid if a female is with the associated male in a location
        It's invalid if a female Fx is together with the opposite male(all but x) in a location

        """

        # -------------------------------------------------
        # Rule 1: boat capacity
        # -------------------------------------------------

        if self.get_num_location( E_location.BOAT ) > 2:
            return True #INVALID

        # -------------------------------------------------
        # Rule 2: female and male
        # -------------------------------------------------
        # for all pairs, if the male and female are in same place, that's valid

        
        if self.ln_location[E_agent.MA] == self.ln_location[E_agent.FA] and self.ln_location[E_agent.MB] == self.ln_location[E_agent.FB] and self.ln_location[E_agent.MC] == self.ln_location[E_agent.FC]:
            return False #VALID
        

        # -------------------------------------------------
        # Rule 3B: female without her paired male, and with a unpaired male
        # -------------------------------------------------
        
        """
        this is overly sensitive, it doesn't count the save from other pairs in the same location
        [0, 0, 0, 1, 0, 0]
        [0, 0, 0, 0, 1, 0]
        [0, 0, 0, 0, 0, 1]
        """

        """
        #if the female is not with her paired male
        if self.ln_location[E_agent.FA] != self.ln_location[E_agent.MA]:
            #and the female is with an unpaired male
            if self.ln_location[E_agent.FA] == self.ln_location[E_agent.MB]:
                return True #INVALID  
            if self.ln_location[E_agent.FA] == self.ln_location[E_agent.MC]:
                return True #INVALID  


        if self.ln_location[E_agent.FB] != self.ln_location[E_agent.MB]:
            #and the female is with an unpaired male
            if self.ln_location[E_agent.FB] == self.ln_location[E_agent.MA]:
                return True #INVALID  
            if self.ln_location[E_agent.FB] == self.ln_location[E_agent.MC]:
                return True #INVALID  

        if self.ln_location[E_agent.FC] != self.ln_location[E_agent.MC]:
            #and the female is with an unpaired male
            if self.ln_location[E_agent.FC] == self.ln_location[E_agent.MA]:
                return True #INVALID  
            if self.ln_location[E_agent.FC] == self.ln_location[E_agent.MB]:
                return True #INVALID  
        """

        # -------------------------------------------------
        # Rule 3: all females together
        # -------------------------------------------------

        
        if self.ln_location[E_agent.FA] == self.ln_location[E_agent.FB] and self.ln_location[E_agent.FA] == self.ln_location[E_agent.FC]:
            return False #VALID
        

        return False #VALID

    def load_boat(self) -> List:
        """
        Enumerate all valid boat loading operations



        """
        
        #number of people on the boat
        n_num_in_boat = self.get_num_location( E_location.BOAT )

        ln_possible_load_move = list()

        if n_num_in_boat >= 2:
            #no move possible
            return ln_possible_load_move

        #for each agent, if that agent is START, make a solution with that agent as boat
        for e_agent in E_agent:
            if self.ln_location[e_agent] == E_location.START:
                ln_copy = self.copy()
                ln_copy.ln_location[e_agent] = E_location.BOAT

                #print(ln_copy)
                #if it's valid
                if ln_copy.is_invalid() == False:
                    #possible load operation
                    ln_possible_load_move.append(ln_copy)

        if n_num_in_boat == 0:
            #for each solution where one was moved
            #for ln_



            #no move possible
            return ln_possible_load_move


        return ln_possible_load_move

    def __str__(self) -> str:
        # converts: [E_location.START, E_location.BOAT, ...]
        # into:     [0, 1, ...]
        return str([int(x) for x in self.ln_location])

def test_bench():

    st_solution = St_solution()

    st_solution.ln_location = [ E_location.START, E_location.START, E_location.START, E_location.START, E_location.START, E_location.START ]

    print(st_solution.is_invalid())


def list_valid_states():

    n_valid : int = 0
    n_invalid : int = 0

    st_solution = St_solution()
    # all possible combinations of 6 positions
    for combo in product(E_location, repeat=6):

        st_solution.ln_location = list(combo)

        # example
        if not st_solution.is_invalid():
            print("VALID:", st_solution.ln_location)
            n_valid += 1
        else:
            n_invalid += 1

    print(f"VALID: {n_valid}")
    print(f"INVALID: {n_invalid}")

def list_valid_load_operation():
    n_valid : int = 0
    n_invalid : int = 0

    st_solution = St_solution()
    lln_load_operation = st_solution.load_boat()

    for ln_load_operation in lln_load_operation:
        print(ln_load_operation)

if __name__ == "__main__":
    #test_bench()

    list_valid_states()

    #list_valid_load_operation()