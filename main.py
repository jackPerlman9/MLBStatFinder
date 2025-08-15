import os
from rich.prompt import Prompt
from datetime import datetime

from util_methods import (
    console,
    get_box_score,
    get_daily_scoreboard,
    get_active_players,
    get_pitcher_matchups,
    get_player_stats 
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    clear_screen()
    console.rule("Menu Options")
    console.print("[bold white]Select an option:[/bold white]")
    console.print("[1] Box Score")
    console.print("[2] Pitcher Matchups")
    console.print("[3] Daily Scoreboard")
    console.print("[4] Player Stats")
    console.print("[5] Quit")

    option1 = Prompt.ask("Enter your choice: ").strip()
    console.print("\n")
    clear_screen()

    # ----- QUIT ------------------
    if option1 == '5':
        console.print("Exiting the program.")
        break

    # ----- PITCHER MATCHUPS ------------------
    elif option1 == '2':
        while True:
            console.rule("Pitcher Matchups!")
            console.print(
                "[bold white]Enter details or select option:[/bold white]\n"
                "[1] Search matchups\n"
                "[2] Back"
            )

            option2 = Prompt.ask("Enter your choice").strip()
            console.print("\n")

            if option2 == '1':
                console.rule("\nPitcher Matchups Search")
                pitcher_name = Prompt.ask("Enter pitcher name")
                opposing_team = Prompt.ask("Enter opposing team abbreviation").upper()
                clear_screen()
                get_pitcher_matchups(pitcher_name, opposing_team)
                Prompt.ask("\nPress Enter to continue...")

            elif option2 == '2':
                break
            else:
                console.print("[red]Invalid option. Please try again.[/red]")

            Prompt.ask("\nPress Enter to continue...")  # Pause before clearing

    # ----- PLAYER PROPS ------------------
    elif option1 == '1':
        console.rule("Box Score!")
        game_id = input("Enter a game ID [YYYYMMDD_AWAY@HOME]: ")
        get_box_score(game_id)
        Prompt.ask("\nPress Enter to continue...")  # Pause before clearing

    # ----- DAILY SCOREBOARD ------------------
    elif option1 == '3':
        while True:
            console.rule("Daily Scoreboard")
            date = Prompt.ask("Enter date (YYYYMMDD format)", default=datetime.now().strftime("%Y%m%d"))
            game_list = get_daily_scoreboard(date)
            
            if game_list:
                console.print("\n[bold white]Select an option:[/bold white]")
                console.print("Enter game number to view box score")
                console.print("Enter 'b' to go back")
                
                choice = Prompt.ask("Your choice").strip().lower()
                
                if choice == 'b':
                    break
                
                try:
                    game_idx = int(choice) - 1
                    if 0 <= game_idx < len(game_list):
                        clear_screen()  # Clear screen before showing box score
                        selected_game_id = game_list[game_idx]
                        console.rule(f"Box Score - Game {game_idx + 1}")
                        get_box_score(selected_game_id)
                        Prompt.ask("\nPress Enter to continue...")
                        clear_screen()  # Clear screen after viewing box score
                    else:
                        console.print("[red]Invalid game number[/red]")
                        Prompt.ask("\nPress Enter to continue...")
                except ValueError:
                    console.print("[red]Invalid input[/red]")
                    Prompt.ask("\nPress Enter to continue...")
            else:
                console.print("[red]No games available for this date[/red]")
                Prompt.ask("\nPress Enter to continue...")
                break
    # ----- PLAYER STATS  ------------------
    elif option1 == '4':
        console.rule("Player Stats!")
        player_name = Prompt.ask("Enter player name to search")
        playerID = get_active_players(player_name)
        if playerID:
            console.print(f"[bold green]Player ID found:[/bold green] {playerID}")
            console.print("\n[bold white]Select an option:[/bold white]")
            console.print("[1] Last Game")
            console.print("[2] 5 Games")
            console.print("[3] 10 Games")
            console.print("[4] Back")
            option2 = Prompt.ask("Enter your choice").strip()

            if option2 == '1':
                console.rule("Last Game Stats")
                get_player_stats(playerID, 1)
            elif option2 == '2':
                console.rule("Last 5 Games Stats")
                get_player_stats(playerID, 5)
            elif option2 == '3':
                console.rule("Last 10 Games Stats")
                get_player_stats(playerID, 10)
            elif option2 == '4':
                continue
            Prompt.ask("\nPress Enter to continue...")
        else:
            console.print("[red]No player found with that name or ID.[/red]")
    else:
        console.print("[red]Invalid option. Please try again.[/red]")
        Prompt.ask("\nPress Enter to continue...")  # Pause before clearing


