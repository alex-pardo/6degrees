
import random

probs = [10, 15, 24, 1]

tmp = sum(probs)

for i in range(0, len(probs)):
	probs[i] /= float(tmp)

print probs
print sum(probs)
selected = [0, 0, 0, 0]
for x in range(0, 100000):
	r = random.random()
	ranges = [0]
	
	for i in range(0, len(probs)):
		ranges.append(ranges[i]+probs[i])
		if r <= (ranges[i]+probs[i]) and r > ranges[i]:
			selected[i] += 1

tmp = sum(selected)
for i in range(0, len(selected)):
	selected[i] /= float(tmp)

print selected

