import random
from FourthRefactoredMonkey import *


nets = [neural_net([1,5,1]) for i in range(100)]
tester = [[[0,]],[[1]]]
answer = [[0],[1]]

for i in range(10000):
    for j in nets:
        scorer = []
        for chooser in range(len(tester)):
            j.activate(tester[chooser])
            scorer.append((j.z[0][0]-answer[chooser][0]) ** 2)
        j.score = sum(scorer)
    nets.sort(key = lambda x: x.score)
    if i % 1000 == 0:
        print("Epoch: " + str(i) + " Score: " + str(nets[0].score))
    for j in range(1,len(nets)):
        parent = random.choice([nets[a] for a in range(0,50)])
        otherparent = random.choice([nets[a] for a in range(0,50)])
        nets[j] = mate(parent,otherparent)

print(nets[0].score)
        