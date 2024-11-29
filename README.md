# NBA-Score-Predictor

This is my final project for the course 'Introduction to Machine Learning' taught by Prof. Sandeep Juneja in Monsoon 2024.

## Objective

Predict the final score of a basketball game between two custom teams composed of NBA All-Star players from 2000 to 2023.

## How-To:

The project's entire contents are in the `main.py` file. Player selection is done via editing the `team_one_players` and `team_two_players` arrays.
The list of required libraries to run this project are:

1. `pandas`
2. `scikit-learn`
3. `xgboost`

Once player selection is complete and libraries are installed, the file can be run just like any other Python program. The output will be visible in the terminal.

## Sample Outpu:

During data processing: `Processing players...`

After player processing and model selection: `Processing complete. All players have been evaluated :)`

Displaying Scores:

Team One:

Predicted score for Stephen Curry: 27

Predicted score for Mo Williams: 15

Predicted score for Ben Simmons: 14

Predicted score for Ja Morant: 22

Predicted score for LaMelo Ball: 16

Team Two:

Predicted score for Klay Thompson: 20

Predicted score for LeBron James: 26

Predicted score for Shaquille O'Neal: 15

Predicted score for Zion Williamson: 23

Predicted score for Yao Ming: 20

Final score: 94 - 104

Team Two Wins!
