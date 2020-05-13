import time
import z3

sigma = lambda n: int(n/2.0 * (1 + n))
"""Arithmetic sum function"""

class PyramidSolver:
    def __init__(self, rows):
        self.rows   = rows
        """Rows in the pyramid"""
        self.data   = list(range(1, sigma(ROWS)+1, 1))
        """The actual data (placeholders)"""
        self.solver = z3.Solver()
        """The Z3 solver"""
        self.syms   = {}
        """Symbols for each slot in the pyramid"""


    def print_pyramid(self):
        """Display the inverted pyramid"""
        R = self.rows
        p = list(self.data); p.reverse()
        r = R
        indent = 0
        max_width = len(str(p[0]))
        nb_fmt = "%%%dd " % (max_width + 1)
        for n in p:
            if r == 0:
                R -= 1
                r = R
                indent += max_width
                print()
                print(' ' * indent, end='')
            r -= 1
            print(nb_fmt % n, end='')

        print()


    def walk_pyramid(self, cb=None):
        """Walks the pyramid and invokes a callback"""
        p = self.data
        R = self.rows
        while R > 0:
            base      = sigma(R)   - 1
            next_base = sigma(R-1) - 1
            if cb is None:
                print("*ROW=%d*" % R)
            offset = -1
            limit  = R - 2
            while offset < limit:
                offset += 1
                a, b, c = p[base - offset], p[base - offset - 1], p[next_base - offset]
                if cb is None:
                    print("|[%d] - [%d]|==[%d]" % (a, b, c))
                else:
                    cb(a, b, c)
            R -= 1

    def get_sym(self, n):
        """Returns a new or previous symbol for the position 'n'"""
        try:
            sym = self.syms[n]
        except:
            sym = self.syms[n] = z3.Int('n_%d' % n)

        return sym

    
    def add_constraints(self, a, b, c):
        """Callback for the walk_pyramid function that creates the proper constraints"""
        syms = [self.get_sym(a), self.get_sym(b), self.get_sym(c)]
        self.solver.add(z3.Or(syms[0] - syms[1] == syms[2], syms[1] - syms[0] == syms[2]))


    def solve(self):
        start_time = time.time()
        # First, create all the symbols the pyramid
        self.walk_pyramid(self.add_constraints)
        # All symbols are distinct
        self.solver.add([z3.Distinct([sym for sym in self.syms.values()])])
        # All symbols range from 1 to sigma(rows)
        self.solver.add([z3.And(s >= 1, s <= len(self.data)) for s in self.syms.values()])

        if self.solver.check() != z3.sat:
            end_time = time.time()
            print("\nUnsolved! Spent, %2.3f second(s)" % (end_time - start_time))
            return False

        model = self.solver.model()
        for n in self.syms.keys():
            sym = model[self.get_sym(n)]
            val = sym.as_long()
            self.data[n-1] = val

        end_time = time.time()
        self.print_pyramid()
        print("\nSolved in %2.3f second(s)" % (end_time - start_time))
        return True

# How many rows the pyramid has
print("Inverted Pyramid Solver using Z3\n\n")

while True:
    ROWS = int(input("Enter how many rows to solve for:"))
    if ROWS <= 1 or ROWS >= 8:
        print("Invalid rows. Must be between [2..8]")
        continue
    break

print("Attempting to solve the pyramid with %d rows, please wait..." % ROWS)
p = PyramidSolver(ROWS)
#p.print_pyramid()
#p.walk_pyramid()
p.solve()