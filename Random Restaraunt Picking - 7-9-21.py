# -*- coding: utf-8 -*-

"""
script to randomly pick winners until exhaustion with non-uniform odds

takes a list of names and corresponding entries
calculates percent chance of winning from straight draw (#of entries/total qualified entries)

randomly chooses winner
removes winner and recalculates odds for subsequent round

chooses winners until no more winners are left

outputs file to selected text location, also prints winners odds of winning for round they won
7-5-21 - updates
edits to include dependencies on Pandas for table manipulation and OS for file management
###now it prints without all the extra 

7-9-21 - updates
adding in date column to automatically assign date
REQUIRES UPLOAD FILE IN SPECIFIC DATE FORMAT

"""
#import csv
import numpy as np
import pandas as pd
import os
import datetime


file_path = r'C:\Users\Kevin\OneDrive\xspam1984\OneDrive\Documents\Python Scripts\Restaraunts\\'

#get the curent date for file saving
today = str(datetime.date.today())
today_date = datetime.date.today()    #non string version

file_name = r"Hagerstown restaraunts "+ today+".csv"
output_file_name = r'Hagerstown List '+ today + ".csv"

#read the csv as a pandas file
df_entries = pd.read_csv(os.path.join(file_path,file_name),encoding = 'ANSI')
#---------------------------------------------------------------------------
entries = df_entries.values.tolist()
for i in entries:
    Names.append(i[0])
    Chances.append(i[1])
    
Names = []
Chances = []
Winners = []
winner_list=[]
winner_prob = []
#---------------------------------------------------------------------------    
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
    #return(draw.astype(str),prob)
    return(' '.join(map(str,draw)),prob)

#given the winner of a previous draw, delete winner from next round of picking;
#permanently alters name, chance and probability
def remove_winner(Names,Chances, probability,winner):
    removal = Names.index(winner)
    
    Names.pop(removal)
    Chances.pop(removal)
    probability.pop(removal)
    
    return(Names, Chances, probability)
      
#generate a new date for a recurring datenight
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

#############################################################################

#main body function that runs while there are still names on the list (haven't been removed as winner)
#create a list of the initial probabilities for reference
initial_prob = Chance_calculator(Chances)
for i in entries:
    i.append(initial_prob[entries.index(i)])

while len(Names) > 0:
    probability = Chance_calculator(Chances)
    (winner , prob) = pick_next_winner(Names, probability)
    #winner_list.append([np.array_str(winner), round(prob,3)])
    winner_list.append([winner, round(prob,3)])
    (Names, Chances, probability) = remove_winner(Names, Chances, probability, winner)

#need to start the list with the first datenight
date_list = [next_weekday(today_date,2)]
#create a list of dates (wednesdays = 2 in function call) for when to have datenight
for i in range((len(winner_list)-1)):
    next_date_night = next_weekday(date_list[-1],2)
    date_list.append(next_date_night)
    

#convert the list to a pandas table to fix formating issues
df_winner_list = pd.DataFrame(winner_list, columns=['Location','Probability of Choice'])
df_winner_list['Date'] = date_list


print(df_winner_list.loc[0])
df_winner_list.to_csv(os.path.join(file_path,output_file_name),index=False)

