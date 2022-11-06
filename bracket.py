import math


# Return a Bracket (array) with num teams
def generate_bracket(num):
    num_rounds = math.log(num, 2)
    if num_rounds != math.trunc(num_rounds):
        raise ValueError("Number of teams must be a power of 2")
    teams = 1
    result = [1]
    while teams != num:
        teams *= 2
        result = tournament_round(teams, result)
    return flatten_list(result)


# Makes the bracket array 1d
def flatten_list(matches):
    teamList = []
    for team_or_match in matches:
        if type(team_or_match) == type([]):
            teamList += flatten_list(team_or_match)
        else:
            teamList += [team_or_match]
    return teamList


# Helper to add a layer to the bracket
def tournament_round(no_of_teams, matchlist):
    new_matches = []
    for team_or_match in matchlist:
        if type(team_or_match) == type([]):
            new_matches += [tournament_round(no_of_teams, team_or_match)]
        else:
            new_matches += [[team_or_match, no_of_teams + 1 - team_or_match]]
    return new_matches
