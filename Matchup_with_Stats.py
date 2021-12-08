import random
import math

#stats of the teams
teams = ['A', 'B']
offense = [80, 50]
defense = [80, 50]

#function to simulate the number of goals scored
def goal_scored(attack, defense):
	score = 0
	check = True
	chance = min(attack/defense*0.5, 1)
	while (check == True):
		n = random.random()
		if(n < chance):
			score += 1
			chance = 0.8 * chance  
		else:
			check = False
	
	return score

#initial values for simulation results
winAAvg = 0
winBAvg = 0 
drawAvg = 0

#simulating 100 games
for j in range(100):
	winA = 0
	winB = 0
	draw = 0
	for i in range(100):
		#simulate the number of goals scored in the match
		scoreA = goal_scored(offense[0], defense[1])
		scoreB = goal_scored(offense[1], defense[0])
		#check the result
		if(scoreA > scoreB):
			winA += 1
		elif(scoreB > scoreA):
			winB += 1
		else:
			draw += 1 
		
		#optional: print the score of the match
		# print( str(scoreA) + " - " + str(scoreB) )

	#optional: print out the current number of wins for each team
	# print('A won: ' + str(winA))
	# print('B won: ' + str(winB))
	# print('Draw: ' + str(draw))
	# print( '\n')
	
	#calculate the average winrates
	winAAvg = (winAAvg*j + winA)/(j+1)
	winBAvg = (winBAvg*j + winB)/(j+1)
	drawAvg = (drawAvg*j + draw)/(j+1)


print('Average win A: ' + str(winAAvg))
print('Average win B: ' + str(winBAvg))
print('Average draw: ' + str(drawAvg))
		
