# NBA-Score-Predictor

This is my final project for the course 'Introduction to Machine Learning' taught by Prof. Sandeep Juneja in Monsoon 2024.

## Objective

Given a list of All-Star NBA players from 2000-2023, the user can select 2 teams of 5 players of their choosing. The model then aims to predict the final score based on player-aggregated data.

## Data Collection

I built a web scraper to extract the All-Star Players from the stipulated year range; it scrapes data from [Basketball-Reference.com](https://www.basketball-reference.com/), and returns player names, the year they played, and the team they played for. Next, I removed all duplicate names and logged the number of times every player has participated in an All-Star match, along with the latest All-Star match they played. After that, I built a web scraper to find the individual player data for each game in the entire season wherein the player went on to play in an All-Star game.
For instance, Karl-Anthony Towns' latest All-Star game was in 2022, so the data collected for him was from every game in the regular 2021-2022 season.

The individual data collected from each player for each game was:

1. Points per game
2. Field Goal %
3. Three Pointer Field Goal %
4. Free Throw %
5. Offensive Rebounds
6. Turnovers

Why collect game-level data from the latest season? The player made it to the All-Star list in that particular season due to their performance over the entire season- this ensures no degradation of performance. The choice of 'most recent All-Star game' is to maintain a semblance of fairness- it seems the simplest way to compare players from the 2000s to the 2020s.
