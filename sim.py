'''
MTQ Lineup Simulator

Create a single elim bracket with 2^x people.

#Use Data from Offcurve.com to determine probability of expected lineups.

Using HSReplay Matchup Data determine probability of each person winning.
'''

import random
import csv
import bracket

d4 = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [2, 4, 5, 6]]


class Tournament:
    def __init__(self, nteams, bo):
        self.nteams = nteams
        self.bracket = bracket.generate_bracket(nteams)
        self.bo = bo-1
        d4copy = d4.copy()
        for i in range(int((nteams/4)-1)):
            d4copy.extend(d4)
            print(d4copy)
        self.lineups = d4copy

    # Simulate the Entire Tournament and return a winner
    def simulate_tourney(self):
        i = 1
        while len(self.bracket) > 1:
            print("round ", i)
            print("bracket ", self.bracket)
            self.bracket = self.simulate_round()
            i += 1
        print("winner is player", self.bracket[0])

    # Simulate all the games in a round
    def simulate_round(self):
        i = 0
        result = []
        while i < len(self.bracket):
            winner = self.simulate_match(self.bracket[i], self.bracket[i + 1])
            result.append(winner)
            i += 2
        return result

    # Repeating the biased coin flip n times to get an estimate on the result of a match
    def simulate_match(self, i, j):
        # probability of player 1 to win
        # Due to the nature of variance in a card game.
        # Use N = 21 biased coin flips to estimate an outcome of a certain game
        p = self.calcp(i, j)
        N = 21
        flips = [flip(p) for i in range(N)]
        odd = float(flips.count('H')) / N
        if odd > 0.5:
            winner = i
        else:
            winner = j

        return winner

    # Determine the deck you would like to ban from your opponent
    # It will be the deck that has the best matchups into your decks
    def ban(self, lu1, lu2, data):
        loseodds = []  # odds of each opponent deck getting a win

        for n in range(self.bo):  # for each of your opponents decks
            p = 0
            deck = lu2[n - 1]
            for m in range(self.bo):  # probability of it beating your deck
                oppDeck = lu1[m - 1]
                p += data[oppDeck - 1][deck - 1]
            loseodds.append(p / self.bo)

        # find deck that is most likely to win
        # return a list without that deck because it will be banned
        max_value = max(loseodds)
        idx = loseodds.index(max_value)
        lu2.pop(idx)
        return lu2

    # Calculate probability of winning based on the match-up table
    def calcp(self, i, j):
        # Possible lineups
        darr = self.lineups
        # Convert CSV file containing match-up data into a array
        with open('matchup_test .csv', newline='') as csvfile:
            data = list(csv.reader(csvfile))

        for row in data:
            for x in range(len(row)):
                row[x] = float(row[x])

        mu_table = data
        odds = []

        lu1 = self.ban(darr[i - 1].copy(), darr[j - 1].copy(), data)
        lu2 = self.ban(darr[j - 1].copy(), darr[i - 1].copy(), data)

        for n in range(self.bo-1):  # for each of your decks
            p = 0
            deck = lu1[n - 1]
            for m in range(self.bo-1):  # for each of your opponents decks calculate probability that your deck gets a win
                odeck = lu2[m - 1]
                p += mu_table[deck - 1][odeck - 1]
            odds.append(p / (self.bo-1))

        result = sum(odds) / len(odds)
        print("p is = ", result)
        return result


# Perform a biased coin flip
def flip(p):
    return 'H' if random.random() < p else 'T'


while True:
    nplayers = int(input("# Players (Multiple of 4) : "))
    if not nplayers%4 == 0:
        print("Must be a multiple of 4")
        continue
    else:
        break

while True:
    bo = int(input("BO3 or BO5 : "))
    if bo not in (3, 5):
        print("only BO3 and BO5 are supported")
        continue
    else:
        break


t = Tournament(nplayers, bo)
t.simulate_tourney()
