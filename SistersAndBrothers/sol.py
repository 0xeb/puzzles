import z3
# Create a solver instance
s = z3.Solver()
# Create two variables representing the total number of males and females (m and f)
m, f = z3.Ints('m f')
# The brother said: I have as many brothers as sisters
s.add(m - 1 == f)
# The sister said: I have twice as much brothers as I have sisters
s.add(2 * (f - 1) == m)
# Check for the solution
if s.check() == z3.sat:
  sol = s.model()
  print("Brothers: %d, Sisters: %d" % (sol[m].as_long(), sol[f].as_long()))