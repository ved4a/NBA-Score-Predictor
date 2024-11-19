# NBA-Score-Predictor

This is my final project for the course 'Introduction to Machine Learning' taught by Prof. Sandeep Juneja in Monsoon 2024.

## Objective

Given a list of All-Star NBA players from 2000-2023, the user can select 2 teams of 5 players of their choosing. This project then aims to predict the final score based on player-aggregated data.

## Data Collection

I've built a web scraper to extract the All-Star Players from the stipulated year range; it scrapes data from [Basketball-Reference.com](https://www.basketball-reference.com/), and returns player names, the year they played, and the team they played for. I'll then use this to create a comprehensive player list that removes any duplicates, and checks how many All-Star games a player has taken part in.

After this, I’ll build another web scraper that finds the following individual player data:

1. y: Points per game
2. X:
   1. Offensive Rebound Percentage (ORB%)
   2. Assists
   3. Shooting Percentage
   4. Free Throw Factor
   5. Number of All-Star Matches Previously Played

X and y will be trained on data from 8 years up to the player’s latest All-Star game, ie: LeBron’s latest All-Star game was in 2023, so performance will be checked from 2015 onwards.

Why 8 years? According to the paper [Understanding High Achievement: The Case for Eminence](https://www.researchgate.net/publication/335431217_Understanding_High_Achievement_The_Case_for_Eminence), the mean career length of an NBA player is 8.2 years.

## Data Aggregation:

Typically, the averages of each statistic are calculated using the statistics of the previous _n_ games. In order to do this, however, several things must first be considered:

1. How many games need to be considered in order to represent a player’s true performance levels?
2. Is the focus solely on individual player data?

Instead of taking the average performance of a player across _n_ games, implementing a weightage system may prove more effective. Players can improve or decline in form as the season progresses, so a simple average may not reflect their improvement or degradation. A potential fix would be to place a higher weightage for the last _y_ games, while applying decaying weight for the rest _x - y_ games.

The NBA has frequent movement of players between teams, even during active seasons. Ultimately, each team is composed of players that determine the strength of each team; there exists a lack of a unifying factor that determines the base power for each team. Thus, the players’ individual performance will be considered in determining their overall strength, and their marginal addition to the user-created team’s strength (aka, how much they contribute to team strength).
