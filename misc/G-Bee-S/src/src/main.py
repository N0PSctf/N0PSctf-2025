import random
import numpy as np
import math
import time

REFERENCE_SCORE = 1322.4725943295052

flowers = []

with open("flowers.txt", 'r') as f:
    for line in f.readlines():
        flowers.append((int(line.split(" ")[0]), int(line.split(" ")[1])))

num_flowers = len(flowers)

data = input("Enter the path Valentine should follow:\n>>> ")
path = data.split(" ")
try:
    for i in range(len(path)):
        path[i] = int(path[i])
        assert path[i] >= 0
except:
    print("The path contains non positive integers or non integers values")
    exit()

try:
    for i in range(51):
        assert i in path
except:
    print("The path does not contain all flowers")
    exit()

try:
    for i in range(1,51):
        assert path.count(i) == 1
    assert path.count(0) == 2
except:
    print("The path covers one flower multiple times or more than two times the beehive")
    exit()

try:
    assert path[0] == 0 and path[-1] == 0
except:
    print("The path does not start or does not end at the beehive.")
    exit()

graph = np.zeros((num_flowers+1,num_flowers+1))

dists = np.zeros(num_flowers+1)
for i in range(len(flowers)):
    dists[i+1] = np.sqrt((flowers[i][0])**2 + (flowers[i][1])**2)
graph[0] = dists

for i in range(len(flowers)):
    dists = np.zeros(num_flowers+1)
    dists[0] = graph[0][i+1]
    for j in range(len(flowers)):
        dists[j+1] = np.sqrt((flowers[j][0]-flowers[i][0])**2 + (flowers[j][1]-flowers[i][1])**2)
    graph[i+1] = dists

score = 0
current_node = 0
for i in path:
    score += graph[current_node][i]
    current_node = i
score += graph[current_node][0]

print(f"The length of your path is {score}.")

if score <= 1400:
    print("Well done! Thanks to you, Valentine can visit all the waterlillies <3\nHere is your flag: N0PS{w4t3rl1ll13s_f0r_v4l3nt1n3}")
else:
    print("Nooooo, this path is too long :'(")