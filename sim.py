'''
MTQ Lineup Simulator

Create a single elim bracket with 2^x people.


#Use Data from Offcurve.com to determine probability of expected lineups.

Using HSReplay Matchup Data determine probability of each person winning.




'''

import math
import random
import csv


# Helper to add a layer to the bracket
def tournament_round(no_of_teams, matchlist):
    new_matches = []
    for team_or_match in matchlist:
        if type(team_or_match) == type([]):
            new_matches += [tournament_round(no_of_teams, team_or_match)]
        else:
            new_matches += [[team_or_match, no_of_teams + 1 - team_or_match]]
    return new_matches


# Makes the bracket array 1d
def flatten_list(matches):
    teamlist = []
    for team_or_match in matches:
        if type(team_or_match) == type([]):
            teamlist += flatten_list(team_or_match)
        else:
            teamlist += [team_or_match]
    return teamlist


# Return a Bracket (array) with num teams
def generate_tournament(num):
    num_rounds = math.log(num, 2)
    if num_rounds != math.trunc(num_rounds):
        raise ValueError("Number of teams must be a power of 2")
    teams = 1
    result = [1]
    while teams != num:
        teams *= 2
        result = tournament_round(teams, result)
    simulate_tourney(flatten_list(result))
    return


# Simulate all the games in a round
def simulate_round(arr):
    i = 0
    result = []
    while i < len(arr):
        winner = simulate_match(arr[i], arr[i+1])
        result.append(winner)
        i += 2
    return result


# Calculate probability of winning based on the match-up table
def calcp(i, j):
    # Possible lineups
    darr = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [2, 4, 5, 6]]

    # Convert CSV file containing match-up data into a array
    with open('matchup_test .csv', newline = '') as csvfile:
        data = list(csv.reader(csvfile))

    for row in data:
        for x in range(len(row)):
            row[x] = float(row[x])

    mu_table = data
    c = []
    for n in range(4):
        p = 0
        deck = darr[i-1][n]
        for m in range(4):
            odeck = darr[j-1][m]
            p += mu_table[deck-1][odeck-1]
        c.append(p/4)

    result = sum(c)/len(c)
    print("p is = ", result)
    return result


# Perform a biased coin flip
def flip(p):
    return 'H' if random.random() < p else 'T'


# Repeating the biased coin flip n times to get an estimate on the result of a match
def simulate_match(i, j):
    # probability of player 1 to win
    # Due to the nature of variance in a card game.
    # Use N = 21 biased coin flips to estimate an outcome of a certain game
    p = calcp(i, j)
    N = 21
    flips = [flip(p) for i in range(N)]
    odd = float(flips.count('H'))/N
    if odd > 0.5:
        winner = i
    else:
        winner = j

    return winner


# Simulate the Entire Tournament and return a winner
def simulate_tourney(arr):
    i = 1
    while len(arr) > 1:
        print("round ", i)
        print("bracket ", arr)
        arr = simulate_round(arr)
        i += 1
    print("winner is player", arr[0])


generate_tournament(4)