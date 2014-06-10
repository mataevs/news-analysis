import random

index = [i for i in range(0,238)]
random.shuffle(index)
f = open('tmp/pos_order.txt', 'w')
for i in index:
	f.write(str(i))
	f.write('\n')
f.close()


index = [i for i in range(0,194)]
random.shuffle(index)
f = open('tmp/neg_order.txt', 'w')
for i in index:
	f.write(str(i))
	f.write('\n')
f.close()