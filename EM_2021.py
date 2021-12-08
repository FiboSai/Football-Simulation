import random
import numpy as np

#groups
group_A = ['Turkey', 'Italy', 'Wales', 'Switzerland']
group_B = ['Denmark', 'Finland', 'Belgium', 'Russia']
group_C = ['Netherlands', 'Ukraine', 'Austria', 'North Macedonia']
group_D = ['England', 'Croatia', 'Scotland', 'Czech Republic']
group_E = ['Spain', 'Sweden', 'Poland', 'Slovakia']
group_F = ['Hungary', 'Portugal', 'France', 'Germany']

all_teams = group_A + group_B + group_C + group_D + group_E + group_F

#rank of each team, initially 0
rank = np.zeros(24,dtype=int)

#winrate matrix
winrate = 0.5*np.ones([24,24], dtype=float)

#brackets, initially empty
round_16 = []
round_8 = []
semi = []
small_final = []
final = []

#function for simulating a group stage
def group_round(teams, winrate): 
	n = len(teams)

	#lists to hold the results of the simulation
	first_place = [0,0,0,0]
	second_place = [0,0,0,0]
	qualified = [0,0,0,0]
	total_points = [0,0,0,0]

	#simulate group matches 
	#create a new array to hold the points for each iteration
	points = [0,0,0,0]
	for i in range(1,n):
		for j in range(0,i):
			#determine the draw range
			draw_range = min(1-winrate[i][j], winrate[i][j])/2
			#generate random number to simulate match
			result = random.random()
			#case where i wins
			if result <= winrate[i][j]-draw_range:
				points[i] += 3
				total_points[i] += 3
			#case where j wins
			elif result >= winrate[i][j] + draw_range: 
				points[j] += 3
				total_points[j] += 3 
			#case where the match results in a draw
			else: 
				points[i] += 1 
				points[j] += 1
				total_points[i] += 1
				total_points[j] += 1
	
	#add small random numbers to create a random tiebreaker 
	for i in range(n):
		points[i] += random.uniform(0,0.1) 
	
	#generate the table 
	rank = sorted(range(len(points)),key=points.__getitem__, 
	reverse=True)
	
	results = []
	for i in range(n):
		results.append((teams[rank[i]], points[rank[i]]))
	
	return results

#function for simulating knockout matches
def knockout(team1, team2, winrate):
	x = random.random()
	#team1 wins
	if x <= winrate:
		winner = team1
		loser = team2
	#team2 wins
	else: 
		winner = team2
		loser = team1 
	return [winner, loser]

#generate results of the group stage 
results_A = group_round(group_A, winrate[0:4,0:4])
results_B = group_round(group_B, winrate[4:8,4:8])
results_C = group_round(group_C, winrate[8:12,8:12])
results_D = group_round(group_D, winrate[12:16,12:16])
results_E = group_round(group_E, winrate[12:20,16:20])
results_F = group_round(group_F, winrate[20:24,20:24])

#find third place finishers
thirds = [results_A[2], results_B[2], results_C[2], 
results_D[2], results_E[2], results_F[2]]

#order them by points
best_thirds = sorted(thirds, key=lambda x: x[1], reverse=True)

#find the 4 best third place finishers
index_thirds = []
for i in range(4):
	index_thirds.append(thirds.index(best_thirds[i]))

#returns the index of the groups with the best thrid place finishers
index_thirds = sorted(index_thirds)

#matrix to determine which teams play each other in the round of 16
qualification_matrix = [[0,1,2,3,0,3,1,2], [0,1,2,4,0,4,2,3], 
[0,1,2,5,0,5,2,3],
[0,1,3,4,3,4,0,1], [0,1,3,5,3,5,0,1], [0,1,4,5,4,5,1,0],
[0,2,3,4,4,3,2,0], [0,2,3,5,5,3,2,0], [0,2,4,5,4,5,2,0],
[0,3,4,5,4,5,3,0], [1,2,3,4,4,3,1,2], [1,2,3,5,5,3,2,1],
[1,2,4,5,5,4,2,1], [1,3,4,5,5,4,3,1], [2,3,4,5,5,4,3,2]]

#determines the correct version of the rounds of 16
for i in range(15):
	if qualification_matrix[i][0:4] == index_thirds:
		third_matches = qualification_matrix[i][4:8]
	i += 1
	
#create round of 16 matches
#Bukarest
round_16.append(results_F[0][0])
round_16.append(thirds[third_matches[3]][0])

#Copenhagen
round_16.append(results_D[1][0])
round_16.append(results_E[1][0])

#Bilbao
round_16.append(results_B[0][0])
round_16.append(thirds[third_matches[0]][0])

#London
round_16.append(results_A[0][0])
round_16.append(results_C[1][0])

#Budapest
round_16.append(results_C[0][0])
round_16.append(thirds[third_matches[1]][0])

#Amsterdam
round_16.append(results_A[1][0])
round_16.append(results_B[1][0])

#Glasgow
round_16.append(results_E[0][0])
round_16.append(thirds[third_matches[2]][0])

#Dublin
round_16.append(results_D[0][0])
round_16.append(results_F[1][0])

#simulate round of 16 
for k in range(8):
	team1 = round_16[2*k]
	team2 = round_16[2*k+1]
	i = all_teams.index(team1)
	j = all_teams.index(team2)
	
	[winner, loser] = knockout(team1, team2, winrate[i][j])
	round_8.append(winner)
	rank[all_teams.index(loser)] = 9

#simulate round of 8 
for k in range(4):
	team1 = round_8[2*k]
	team2 = round_8[2*k+1]
	i = all_teams.index(team1)
	j = all_teams.index(team2)
	
	[winner, loser] = knockout(team1, team2, winrate[i][j])
	semi.append(winner)
	rank[all_teams.index(loser)] = 5

#simulate semifinals
for k in range(2):
	team1 = semi[2*k]
	team2 = semi[2*k+1]
	i = all_teams.index(team1)
	j = all_teams.index(team2)
	
	[winner, loser] = knockout(team1, team2, winrate[i][j])
	small_final.append(loser)
	final.append(winner)

#simulate small final
[third, fourth] = knockout(small_final[0], small_final[1], 
winrate[all_teams.index(small_final[0])][all_teams.index(small_final[1])])
rank[all_teams.index(third)] = 3
rank[all_teams.index(fourth)] = 4

#simulate final 
[champion, runner_up] = knockout(final[0], final[1], 
winrate[all_teams.index(final[0])][all_teams.index(final[1])])
rank[all_teams.index(champion)] = 1
rank[all_teams.index(runner_up)] = 2

#fill in remaining ranks
for k in range(24):
	if rank[k]==0:
		rank[k] = 17

#announce winners
print ('First place: ' + champion)
print ('Second place: ' + runner_up)
print ('Third place: ' + third) 
print ('Fourth place: ' + fourth)
