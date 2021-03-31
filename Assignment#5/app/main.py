from fastapi import FastAPI
from mangum import Mangum
from sympy.ntheory import isprime
from random import randint
import math, decimal

NBA_Teams = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Bobcats","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","LA Clippers","LA Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Hornets","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia Sixers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]
NFL_Teams = ["Arizona Cardinals","Atlanta Falcons","Baltimore Ravens","Buffalo Bills","Carolina Panthers","Chicago Bears","Cincinnati Bengals","Cleveland Browns","Dallas Cowboys","Denver Broncos","Detroit Lions","Green Bay Packers","Houston Texans","Indianapolis Colts","Jacksonville Jaguars","Kansas City Chiefs","Los Angeles Chargers","Los Angeles Rams","Miami Dolphins","Minnesota Vikings","New England Patriots","New Orleans Saints","New York Giants","New York Jets","Oakland Raiders","Philadelphia Eagles","Pittsburgh Steelers","San Francisco 49ers","Seattle Seahawks","Tampa Bay Buccaneers","Tennessee Titans","Washington Redskins"]
EPL_Teams = ["Arsenal","A.F.C. Bournemouth","Brighton & Hove Albion","Burnley","Chelsea","Crystal Palace","Everton","Huddersfield Town","Leicester City","Liverpool","Manchester City","Manchester United","Newcastle United","Southampton","Stoke City","Swansea City","Tottenham Hotspur","Watford","West Bromwich Albion","West Ham United"]

app = FastAPI(title="Sports Teams API")
handler = Mangum(app=app)


def isTeamInNBA(teamNameQuery: str):
    teamsToReturn = []
    for teamName in NBA_Teams:
        if teamNameQuery in teamName:
            teamsToReturn.append(teamName)
    return teamsToReturn

def isTeamInNFL(teamNameQuery: str):
    teamsToReturn = []
    for teamName in NFL_Teams:
        if teamNameQuery in teamName:
            teamsToReturn.append(teamName)
    return teamsToReturn

def isTeamInEPL(teamNameQuery: str):
    teamsToReturn = []
    for teamName in EPL_Teams:
        if teamNameQuery in teamName:
            teamsToReturn.append(teamName)
    return teamsToReturn

def findTeam(teamNameQuery: str):
    teamsToReturn = []
    teamsToReturn.append(isTeamInNBA(teamNameQuery))
    teamsToReturn.append(isTeamInNFL(teamNameQuery))
    teamsToReturn.append(isTeamInEPL(teamNameQuery))
    return teamsToReturn

@app.get("/NBA")
async def get_NBA_teams():
    return {
        'NBAteams': NBA_Teams
    }

@app.get("/NBA/{teamName}")
async def check_NBA_team(teamName: str):
    return {
        'teamNameQueried': teamName,
        'matchingNBAteams': isTeamInNBA(teamName)
    }

@app.get("/NFL")
async def get_NFL_teams():
    return {
        'NFLteams': NFL_Teams
    }

@app.get("/NFL/{teamName}")
async def check_NBA_team(teamName: str):
    return {
        'teamNameQueried': teamName,
        'matchingNFLteams': isTeamInNFL(teamName)
    }

@app.get("/EPL")
async def get_EPL_teams():
    return {
        'NBAteams': EPL_Teams
    }

@app.get("/EPL/{teamName}")
async def check_EPL_team(teamName: str):
    return {
        'teamNameQueried': teamName,
        'matchingEPLteams': isTeamInEPL(teamName)
    }

@app.get("/findTeam/{teamName}")
async def check_EPL_team(teamName: str):
    return {
        'teamNameQueried': teamName,
        'matchingTeams': findTeam(teamName)
    }

@app.post("/add/{league}/{teamName}")
async def addTeamToLeague(league: str,teamName: str):
    if league == "NFL":
        NFL_Teams.append(team)
        return {
            'leagueAddedTo': "NFL",
            'teamNameAdded': teamName,
            'NFL Teams': NFL_Teams
        }
    elif league == "NBA":
        NBA_Teams.append(teamName)
        return {
            'leagueAddedTo': "NBA",
            'teamNameAdded': teamName,
            'NBA Teams': NBA_Teams
        }
    elif league == "EPL":
        EPL_Teams.append(teamName)
        return {
            'leagueAddedTo': "EPL",
            'teamNameAdded': teamName,
            'EPL Teams': EPL_Teams
        }
    else:
        return {
            "Failure": "True"
        }
    
@app.put("/{league}/{teamNameToUpdate}/{NewName}")
async def addTeamToLeague(league: str,teamNameToUpdate: str, NewName: str):
    teams = None
    if league == "NFL":
        teams = NFL_Teams
    elif league == "NBA":
        teams = NBA_Teams
    elif league == "EPL":
        teams = EPL_Teams
    else:
        return {
            "Failure": "True"
        }

    for i, teamName in enumerate(teams):
        if teamName == teamNameToUpdate:
            teams[i]= NewName
    return{
        "UpdateLeageTeams":teams
    }

@app.delete("/{league}/{teamNameToDelete}")
async def addTeamToLeague(league: str,teamNameToDelete: str):
    teams = None
    if league == "NFL":
        teams = NFL_Teams
    elif league == "NBA":
        teams = NBA_Teams
    elif league == "EPL":
        teams = EPL_Teams
    else:
        return {
            "Failure": "True"
        }

    indexToDelete=None
    for i, teamName in enumerate(teams):
        if teamName == teamNameToDelete:
            indexToDelete=i

    if indexToDelete != None:
        teams.pop(indexToDelete)
    return{
        "UpdateLeageTeams":teams
    }