# NBA-Score-Predictor

This is my final project for the course 'Introduction to Machine Learning' taught by Prof. Sandeep Juneja in Monsoon 2024.

## Objective

Given a list of All-Star NBA players from the past 4 years, the user can select 2 teams of 5 players of their choosing. This project then aims to predict the final score based on player-aggregated data.

## Data Collection

I'll be using data from the [NBA Players Dataset](https://www.kaggle.com/datasets/justinas/nba-players-data), created and maintained by Justinas Cirtautas on Kaggle. It was last updated 1 year ago to account for the 2022-2023 season.

## Data Aggregation:

Typically, the averages of each statistic are calculated using the statistics of the previous _n_ games. In order to do this, however, several things must first be considered:

1. How many games need to be considered in order to represent a player’s true performance levels?
2. Is the focus solely on individual player data?
3. What features are relevant?

Instead of taking the average performance of a player across _n_ games, implementing a weightage system may prove more effective. Players can improve or decline in form as the season progresses, so a simple average may not reflect their improvement or degradation. A potential fix would be to place a higher weightage for the last _y_ games, while applying decaying weight for the rest _x - y_ games.

The NBA has frequent movement of players between teams, even during active seasons. Ultimately, each team is composed of players that determine the strength of each team; there exists a lack of a unifying factor that determines the base power for each team. Thus, the players’ individual performance will be considered in determining their overall strength, and their marginal addition to the user-created team’s strength (aka, how much they contribute to team strength).

Based on similar projects, I was able to narrow down the feature selection list. This list has loosely built upon the [Four Factors](https://www.basketball-reference.com/about/factors.html). Tentatively, the feature list will be:

1. Offensive power
   1. Points
   2. Offensive Rebound Percentage (ORB%)
   3. Assists
   4. Shooting Percentage
   5. Free Throw Factor
2. Defensive power
   1. Blocks
   2. Steals
   3. Defensive Rebound Percentage (DRB%)
3. Misc.
   1. Injury Likelihood
   2. Number of All-Star Matches Previously Played
