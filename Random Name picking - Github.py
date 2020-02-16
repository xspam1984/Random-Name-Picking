# -*- coding: utf-8 -*-

"""
script to randomly pick winners until exhaustion with non-uniform odds

takes a list of names and corresponding entries
calculates percent chance of winning from straight draw (#of entries/total qualified entries)

randomly chooses winner
removes winner and recalculates odds for subsequent round

chooses winners until no more winners are left

outputs file to selected text location, also prints winners odds of winning for round they won

"""

import csv
import numpy as np

#expects a data format that has a list of [ names, #of Entries]
with open('C:/xxxx.csv', 'r') as f:
    reader = csv.reader(f)
    entries = list((rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a single list

Names = []
Chances = []
Winners = []
winner_list=[]
winner_prob = []

for i in entries:
    Names.append(i[0])
    Chances.append(i[1])
    
#given an inputed list of entries, calculate the probability of that entry winning by summing up all entries
def Chance_calculator(chances):
    t = 0
    probability = []
    for i in chances:
        t = t + int(i)
    for i in chances:
        probability.append(int(i)/t)
    return(probability)

#given a list of names, and the corresponding probability, choose a winner at random
def pick_next_winner(Names, probability):
    draw = np.random.choice(Names,1,probability)
    tick = Names.index(draw)
    prob = probability[tick]
    return(draw,prob)

#given the winner of a previous draw, delete winner from next round of picking;
#permanently alters name, chance and probability
def remove_winner(Names,Chances, probability,winner):
    removal = Names.index(winner)
    
    Names.pop(removal)
    Chances.pop(removal)
    probability.pop(removal)
    
    return(Names, Chances, probability)
  
    
#main body function that runs while there are still names on the list (haven't been removed as winner)
#create a list of the initial probabilities for reference
initial_prob = Chance_calculator(Chances)
for i in entries:
    i.append(initial_prob[entries.index(i)])

while len(Names) > 0:
    probability = Chance_calculator(Chances)
    (winner , prob) = pick_next_winner(Names, probability)
    winner_list.append([winner, round(prob,3)])
    (Names, Chances, probability) = remove_winner(Names, Chances, probability, winner)

#print(winner_list)

#Save list
with open('C:/xxxx.txt','w') as f:
    writer = csv.writer(f)
    writer.writerows(winner_list)

