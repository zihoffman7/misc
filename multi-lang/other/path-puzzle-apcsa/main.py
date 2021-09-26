factorial = lambda x: 1 if x < 2 else x * factorial(x - 1)
possible_solutions = lambda x: 1 if x < 2 else possible_solutions(x - 1) + (lambda x: (3 * x - 2) * (lambda x: factorial(2 * x) / (factorial(x + 1) * factorial(x)))(x - 1))(x - 1)

print(possible_solutions(100))
