	

def p(limit):
	print(2)
	list = [2]
	maybeFoundPrime = True
	currentNum=3
	howManyPrimes = 0
	while limit >= howManyPrimes:
		for n in list:
			if currentNum%n == 0:
				maybeFoundPrime=False
				break
		if maybeFoundPrime == True:
			list.append(currentNum)
			howManyPrimes += 1
			print(currentNum)
			print(currentNum)
		currentNum = currentNum + 2
		maybeFoundPrime = True
	#return list