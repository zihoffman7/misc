prime = [2, 3]

for i in range(4, 1000):
    for j in prime:
        if i % j == 0:
            prime.append(i)


print(len(prime))
