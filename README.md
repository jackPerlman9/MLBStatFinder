# MLBStatFinder
A command-line interface application that provides real-time MLB statistics and game information. Statistics include Box Scores, Pitcher Matchups, Daily Scoreboard, and Individual Player Statistics.

## External Tools
This project couldn't be done without using Rapid API and their easy to use Data APIs. The one I used for this project is called "Tank01 MLB Live In-Game Real Time Statistics"
If you would like to be able to use this program you must get a free subscription to the API. The link for this is right here:
https://rapidapi.com/tank01/api/tank01-mlb-live-in-game-real-time-statistics

## Usage
The Program can be executed using the .bat file found in the repo. Make sure you create your own .env with your own API Key within it, or else you cannot access the API data. The rest of the program is simple enough, simply follow the command-line prompts and get curious about baseball!

## Features
As of now I have a 4 features to offer:

- <strong>Box Score</strong> <br>
  Enter the GameID to access all the Box Score Info
- <strong>Pitcher Matchups</strong> <br>
  Enter the name of a Pitcher as well as the opposing batting team to pull up every opposing player's statistics against the given pitcher
  (NOTE: I have noticed a bug with Shohei Ohtani where his statistics do not show up properly since he hits and pitches)
- <strong>Daily Scoreboard</strong> <br>
  Enter a Date and you will get the scoreboard of games for that day. This feature is live and will post current scores as the game is ocurring. You can enter the number corresponding to the game and you will be able to see the Box Score of that game even if the game is currently going on
- <strong>Player Stats</strong> <br>
  Enter the name of a hitter and you can see their n number of game statistics. I currently have it capped to a max of 10 previous games but with some change in the code it can be customized.

## Improvements
Of course, Rome wasn't built in a day, and neither was this project. But, here are some improvements that I (or someone else) could make to make this program better:

- General UI Tweaks: While the UI that I have created works well, there are a few minor problems such as the back button taking you back to the first page when instead i want to stay in entering say a Box Score query
- Player Stats Cumulative AVG: When looking at the player's stats for each game, the individual batting average of each game is shown instead of the cumulative batting average of the whole season or from the earliest game that is shown.
- Shohei Ohtani (The one outlier): Since Shohei Ohtani both bats and pitches. I believe the API has an issue with determining whether Ohtani is batting against a pitcher or <strong>IS</strong> the pitcher. Thus, when you search up matchups between batters and Ohtani, you make get weird results...
- New Animations: it can take some time to search up a player within the API's .json file. To combat this, I would like to add a simple loading bar or icon to show that the program is still fetching data (only takes about 6-7 seconds to load player info).
