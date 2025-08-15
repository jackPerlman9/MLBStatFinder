import requests
import json
import os
import http.client
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

# Load environment variables
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# Create console instance at module level
console = Console()

# Make sure to export console and other required functions
__all__ = [
    'console',
    'get_box_score',
    'get_daily_scoreboard',
    'get_active_players'  # Add this line
]

def load_team_colors():
    try:
        with open('team_colors.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading team colors: {str(e)}[/red]")
        return {}

# Load team colors once when module is imported
TEAM_COLORS = load_team_colors()

def get_box_score(game_id):
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBoxScore"
    
    querystring = {
        "gameID": game_id,
        "playerStatsFormat": "list",
        "startingLineups": "true",
        "fantasyPoints": "true"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json().get('body', {})
    
    # Game Info Table
    info_table = Table(title="Game Information", show_header=False)
    info_table.add_column("Info", style="cyan")
    info_table.add_column("Value", style="white")
    
    info_table.add_row("Venue", data.get('Venue', 'N/A'))
    info_table.add_row("Weather", data.get('Weather', 'N/A'))
    info_table.add_row("First Pitch", data.get('FirstPitch', 'N/A'))
    info_table.add_row("Game Length", data.get('GameLength', 'N/A'))
    info_table.add_row("Attendance", data.get('Attendance', 'N/A'))
    
    # Line Score Table
    line_score = data.get('lineScore', {})
    line_table = Table(title="Line Score")
    line_table.add_column("Team", style="cyan")
    
    # Determine max innings from actual game data
    away_scores = line_score.get('away', {}).get('scoresByInning', {})
    home_scores = line_score.get('home', {}).get('scoresByInning', {})
    max_innings = max(
        9,  # minimum 9 innings
        max(
            max(map(lambda x: int(x), away_scores.keys())) if away_scores else 0,
            max(map(lambda x: int(x), home_scores.keys())) if home_scores else 0
        )
    )
    
    # Add inning columns
    for i in range(1, max_innings + 1):
        line_table.add_column(str(i), justify="center", width=3)
    line_table.add_column("R", justify="center", style="green")
    line_table.add_column("H", justify="center")
    line_table.add_column("E", justify="center", style="red")
    
    # Add away team line score
    away_line = [data.get('away', 'Away')]
    for i in range(1, max_innings + 1):
        away_line.append(away_scores.get(str(i), ' '))
    away_stats = line_score.get('away', {})
    away_line.extend([
        away_stats.get('R', '0'),
        away_stats.get('H', '0'),
        away_stats.get('E', '0')
    ])
    line_table.add_row(*[str(x) for x in away_line])
    
    # Add home team line score
    home_line = [data.get('home', 'Home')]
    for i in range(1, max_innings + 1):
        home_line.append(home_scores.get(str(i), ' '))
    home_stats = line_score.get('home', {})
    home_line.extend([
        home_stats.get('R', '0'),
        home_stats.get('H', '0'),
        home_stats.get('E', '0')
    ])
    line_table.add_row(*[str(x) for x in home_line])

    # Team Stats Tables
    def create_team_stats_table(team_stats, team_name):
        stats_table = Table(title=f"{team_name} Team Stats")
        stats_table.add_column("Category", style="cyan")
        stats_table.add_column("Value", style="white")
        
        categories = {
            "Hitting": ["AB", "H", "R", "RBI", "BB", "SO", "HR", "AVG"],
            "Pitching": ["IP", "H", "R", "ER", "BB", "SO", "HR", "Pitches"],
            "BaseRunning": ["SB", "CS"],
            "Fielding": ["E", "Passed Ball"]
        }
        
        for category, stats in categories.items():
            if category in team_stats:
                for stat in stats:
                    value = team_stats[category].get(stat, '0')
                    stats_table.add_row(stat, str(value))
        
        return stats_table
    
    away_stats = data.get('teamStats', {}).get('away', {})
    home_stats = data.get('teamStats', {}).get('home', {})
    
    away_stats_table = create_team_stats_table(away_stats, data.get('away', 'Away'))
    home_stats_table = create_team_stats_table(home_stats, data.get('home', 'Home'))
    
    # Print all tables
    console.print(info_table)
    console.print("\n")
    console.print(line_table)
    console.print("\n")
    console.print(away_stats_table)
    console.print("\n")
    console.print(home_stats_table)
def get_daily_scoreboard(date):
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBScoresOnly"
    
    querystring = {
        "gameDate": date,
        "topPerformers": "true"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    # Create a table to display scores
    table = Table(title=f"MLB Scores for {date}")
    table.add_column("#", style="bold cyan", justify="center")
    table.add_column("Game", style="cyan", justify="left")
    table.add_column("Score", style="green", justify="center")
    table.add_column("Status", style="yellow", justify="right")
    
    # Store game_ids for return
    game_list = []
    
    try:
        games = data.get('body', {})
        if isinstance(games, dict):
            for idx, (game_id, game_info) in enumerate(games.items(), 1):
                away_team = game_info.get('away', 'N/A')
                home_team = game_info.get('home', 'N/A')
                game_status = "Hasn't started"
                # Color the team abbreviations
                away_color = TEAM_COLORS.get(away_team, "#ffffff")
                home_color = TEAM_COLORS.get(home_team, "#ffffff")
                away_colored = f"[{away_color}]{away_team}[/]"
                home_colored = f"[{home_color}]{home_team}[/]"
                
                # Get line scores
                line_score = game_info.get('lineScore', {})
                if line_score and isinstance(line_score, dict):
                    away_data = line_score.get('away', {})
                    home_data = line_score.get('home', {})
                    away_score = away_data.get('R') if away_data else '0'
                    home_score = home_data.get('R') if home_data else '0'
                else:
                    away_score = '0'
                    home_score = '0'
                
                # Format the matchup and score with colored team names
                matchup = f"{away_colored} @ {home_colored}"
                score = f"{away_score}-{home_score}"
                
                # Add status details for live games
                if game_info.get('gameStatusCode') == "1":
                    current_inning = game_info.get('currentInning', '')
                    current_outs = game_info.get('currentOuts', '')
                    game_status = f"{current_inning} ({current_outs} outs)"
                elif game_info.get('gameStatusCode') == "2":
                    game_status = "Final"
                
                table.add_row(str(idx), matchup, score, game_status)
                game_list.append(game_id)
                
    except Exception as e:
        console.print(f"[red]Error processing game data: {str(e)}[/red]")
        return None
    
    console.print(table)
    return game_list

def get_active_players(player_name=None):
    """
    Get a list of all active MLB players with their team and player ID.
    If player_name is provided, returns that player's ID.
    Otherwise returns a dictionary mapping player names to their info.
    """
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBPlayerList"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if player_name:  # If searching for a specific player
            if 'body' in data:
                players = data['body']
                for player_info in players:
                    if player_info.get('longName', '').lower() == player_name.lower():
                        return player_info.get('playerID')
            console.print(f"[red]Player '{player_name}' not found[/red]")
            return None
        
        # Original functionality for listing all players
        table = Table(title="Active MLB Players")
        table.add_column("Player Name", style="cyan")
        table.add_column("Team", style="green")
        table.add_column("Player ID", style="yellow")
        
        players_dict = {}
        
        if 'body' in data:
            players = data['body']
            for player_info in players:
                name = player_info.get('longName', 'N/A')
                team = player_info.get('team', 'N/A')
                player_id = player_info.get('playerID', 'N/A')
                
                players_dict[name] = {
                    'team': team,
                    'playerID': player_id
                }
                
                team_color = TEAM_COLORS.get(team, "#ffffff")
                team_colored = f"[{team_color}]{team}[/]"
                table.add_row(name, team_colored, player_id)
                
        console.print(table)
        return players_dict
    
    except Exception as e:
        console.print(f"[red]Error fetching player list: {str(e)}[/red]")
        return None

def get_pitcher_matchups(pitcher_name, opposing_team):
    """
    Get pitcher vs batter stats for all active players on the opposing team.
    """
    # First get all active players to find pitcher's ID
    url_players = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBPlayerList"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }

    try:
        # Get all players
        response = requests.get(url_players, headers=headers)
        data = response.json()
        
        pitcher_id = None
        opposing_players = []

        if 'body' in data:
            players = data['body']
            # Find pitcher ID and opposing team players
            for player in players:
                if player.get('longName', '').lower() == pitcher_name.lower():
                    pitcher_id = player.get('playerID')
                elif player.get('team') == opposing_team:
                    opposing_players.append({
                        'name': player.get('longName'),
                        'playerID': player.get('playerID')
                    })

        if not pitcher_id:
            console.print(f"[red]Pitcher '{pitcher_name}' not found[/red]")
            return

        # Create matchup stats table
        matchup_table = Table(title=f"Pitcher Matchups: {pitcher_name} vs {opposing_team}")
        matchup_table.add_column("Batter", style="cyan")
        matchup_table.add_column("AB", justify="center")
        matchup_table.add_column("H", justify="center")
        matchup_table.add_column("2B", justify="center")
        matchup_table.add_column("3B", justify="center")
        matchup_table.add_column("HR", justify="center", style = "yellow")
        matchup_table.add_column("RBI", justify="center")
        matchup_table.add_column("BB", justify="center")
        matchup_table.add_column("K", justify="center")
        matchup_table.add_column("AVG", justify="center", style="green")

        # Get matchup stats for each opposing player
        url_matchup = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        
        for batter in opposing_players:
            querystring = {"playerID": pitcher_id, "playerRole": "", "opponent": batter['playerID']}
            response = requests.get(url_matchup, headers=headers, params=querystring)
            matchup_data = response.json()

            if 'body' in matchup_data and 'opponents' in matchup_data['body']:
                # Access the stats from the correct path in the JSON
                stats = matchup_data['body']['opponents'][0]['stats'] if matchup_data['body']['opponents'] else {}
                
                matchup_table.add_row(
                    batter['name'],
                    str(stats.get('AB', '0')),
                    str(stats.get('H', '0')),
                    str(stats.get('2B', '0')),
                    str(stats.get('3B', '0')),
                    str(stats.get('HR', '0')),
                    str(stats.get('RBI', '0')),
                    str(stats.get('BB', '0')),
                    str(stats.get('K', '0')),  
                    str(stats.get('AVG', '.000'))
                )

        console.print(matchup_table)

    except Exception as e:
        console.print(f"[red]Error fetching matchup data: {str(e)}[/red]")
        console.print(f"[yellow]API Response: {matchup_data}[/yellow]")  # Debug info

def get_player_stats(player_id, num_games):
    """
    Get detailed stats for a specific player by their ID.
    """
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBGamesForPlayer"
    
    querystring = {
        "playerID": str(player_id),
        "numberOfGames": str(num_games),
        "season": "2025"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }   

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Check if we have valid data
        if not data.get('body'):
            console.print("[red]No player stats found for the given ID[/red]")
            return None
            
        games_data = data['body']
        
        # Create stats table
        table = Table(title=f"Player Stats for last {num_games} game(s)")
        table.add_column("Game Date", style="cyan", justify="center")
        table.add_column("Team", style="green", justify="center")
        table.add_column("Pos", style="yellow", justify="center")
        table.add_column("AB", justify="center")
        table.add_column("H", justify="center")
        table.add_column("R", justify="center")
        table.add_column("RBI", justify="center")
        table.add_column("BB", justify="center")
        table.add_column("SO", justify="center")
        table.add_column("HR", justify="center", style="yellow")
        table.add_column("AVG", justify="center", style="green")

        # Process each game's stats
        for game_id, game_data in games_data.items():
            if isinstance(game_data, dict):
                hitting_stats = game_data.get('Hitting', {})
                game_date = game_id.split('_')[0]  # Extract date from game_id
                team = game_data.get('team', 'N/A')
                position = game_data.get('startingPosition', 'N/A')
                
                # Color the team name
                team_color = TEAM_COLORS.get(team, "#ffffff")
                team_colored = f"[{team_color}]{team}[/]"
                
                table.add_row(
                    game_date,
                    team_colored,
                    position,
                    str(hitting_stats.get('AB', '0')),
                    str(hitting_stats.get('H', '0')),
                    str(hitting_stats.get('R', '0')),
                    str(hitting_stats.get('RBI', '0')),
                    str(hitting_stats.get('BB', '0')),
                    str(hitting_stats.get('SO', '0')),
                    str(hitting_stats.get('HR', '0')),
                    str(hitting_stats.get('AVG', '.000'))
                )

        console.print(table)
        return games_data

    except Exception as e:
        console.print(f"[red]Error fetching player stats: {str(e)}[/red]")
        return None