array = [23, 631, 0, -343, 0, -1]
min_ = 1000
i = 0
n = 6
stop = n - 1
while i < stop:
	if min_ > array[i]:
		min_ = array[i]
	i = i + 1

print(min_)
