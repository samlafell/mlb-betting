'''
Title: Gather Game Info
Author: Sam LaFell
Date: 11/21/2022
Purpose: Gather Game information into one DF

Granularity: Date/HT/VT -- pitcher xba, batter xba for both teams
'''

# Import Libraries
import pandas as pd
pd.set_option('display.max_columns', 50)
import pybaseball as pb
from pybaseball import statcast, statcast_pitcher, statcast_batter
from datetime import datetime, timedelta
import numpy as np

'''
Data to use:
Statcast
'''

def gather_game_info(game_day, team):
    data = statcast(start_dt=game_day, end_dt=game_day, team=team)
    if data.shape[0] == 0:
        return None
    else:
        return data

def second_team(first_team, game_info_df):
    ########## TO DO for next time, find a better way to grab the teams. This is close to being a good spot ####################
    # Found home team is Miami, run that
    teams = [v for k,v in game_info_df[['home_team', 'away_team']].to_dict().items()]
    team_list = []
    for dict_object in teams:
        team = [v for k,v in dict_object.items()]
        team_list.append(team)
    team_flat = [item for sublist in team_list for item in sublist]
    team2 = [team_iter for team_iter in team_flat if team_iter != first_team]
    return team2[0]

# * Pitchers
def identify_home_away_pitchers(full_game_df):
    
    away_pitcher = full_game_df.loc[(full_game_df['inning'] == 1) & (full_game_df['inning_topbot'] == 'Bot')].pitcher.unique().tolist()[0]
    home_pitcher = full_game_df.loc[(full_game_df['inning'] == 1) & (full_game_df['inning_topbot'] == 'Top')].pitcher.unique().tolist()[0]

    return home_pitcher, away_pitcher

def pitcher_last4weeks(game_day, lookback_period, pitchers:list):
    # Define ranges
    first_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = lookback_period)).strftime('%Y-%m-%d')
    last_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')
    
    # Pull Pitching Information
    pitcher_df = pd.DataFrame()
    for pitcher in pitchers:
        temp_pitch_df = statcast_pitcher(start_dt=first_day_range, end_dt=last_day_range, player_id = pitcher)
        pitcher_df = pd.concat([pitcher_df, temp_pitch_df])
    
    return pitcher_df

def aggregate_pitcherpreformance(pitcher_df, home_pitcher):
    pitchers_df = pitcher_df[['game_date', 'pitcher', 'estimated_ba_using_speedangle']].dropna().groupby(['pitcher']).agg({'estimated_ba_using_speedangle':'median'}).reset_index()
    pitchers_df['home_away'] = np.where(four_week_pitcher_aggregate['pitcher'] == home_pitcher, 'home', 'away')
    pitchers_df.drop('pitcher', axis = 1, inplace=True)
    return pitchers_df

# * Batters
def identify_home_away_batters(full_game_df):
    home_batters = full_game_df.loc[full_game_df['inning_topbot'] == 'Bot'].batter.unique().tolist()
    away_batters = full_game_df.loc[full_game_df['inning_topbot'] == 'Top'].batter.unique().tolist()
    return home_batters, away_batters

def batter_lastfourweeks(game_day, lookback_period, home_batters:list, away_batters:list):
    # Define ranges
    first_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = lookback_period)).strftime('%Y-%m-%d')
    last_day_range = (datetime.strptime(game_day, '%Y-%m-%d') - timedelta(days = 1)).strftime('%Y-%m-%d')
    
    # Pull Batting Information
    home_batter_df = pd.DataFrame()
    for batter in home_batters:
        temp_batting_df = statcast_batter(start_dt=first_day_range, end_dt=last_day_range, player_id = batter)
        home_batter_df = pd.concat([home_batter_df, temp_batting_df])
        
    away_batter_df = pd.DataFrame()
    for batter in away_batters:
        temp_batting_df = statcast_batter(start_dt=first_day_range, end_dt=last_day_range, player_id = batter)
        away_batter_df = pd.concat([away_batter_df, temp_batting_df])
    
    return home_batter_df, away_batter_df

def get_top9batters(batter_df):
    # Get Plate Appearances
    atbats = batter_df.groupby(['game_date', 'batter', 'at_bat_number']).agg({'batter':'nunique'})
    atbats.columns = ['batter_count']
    atbats = atbats.reset_index()
    atbats = atbats.drop(columns=['at_bat_number'], axis=1).groupby('batter').sum(numeric_only=True).reset_index()
    top9 = atbats.loc[atbats['batter_count'].rank(ascending=False).__lt__(10)]
    return top9

def aggregate_batterpreformance(batter_df, only_top9 = True):
    if only_top9==True:
        top9 = get_top9batters(batter_df)['batter'].values.tolist()
        batter_df = batter_df.loc[batter_df['batter'].isin(top9)]

    batter_df_agg = batter_df[['game_date', 'batter', 'estimated_ba_using_speedangle']].dropna().groupby(['batter']).agg({'estimated_ba_using_speedangle':'median'}).reset_index()
    return batter_df_agg


# * Step 1. Define the parameters of our search
# Who do we want to look at
team = 'ATL'
game_day = '2018-05-13'

# * Step 2. Grab the information for the game (id, day, teams)
# Full Statcast Info for the first team of interest
first_team_df = gather_game_info(game_day, team) # this gives all the pitchers that ATL threw, not Miami, that has to be different.
# Describe some basic info like game_id, date, home, and away
game_info = first_team_df[['game_pk', 'game_date', 'home_team', 'away_team']].drop_duplicates()

# * Step 3. Identify the 2nd team, and grab the statcast df for the team as well
# Who is the 2nd team that wasn't initially listed?
second_team = second_team(team, game_info)

# If Team1 was queried in the first function pull, skip it. Then move to team 2.
second_team_df = gather_game_info(game_day, second_team)

# * Step 4. Join the previous two DFs to combine all statcast info
# Append the two dfs
full_game_df = pd.concat([first_team_df, second_team_df])

# * Step 5. Identify Pitchers
home_pitcher, away_pitcher = identify_home_away_pitchers(full_game_df)

# * Step 6. Identify Get all at bats for the pitchers the last x days
pitchers_df = pitcher_last4weeks(game_day, 28, [home_pitcher, away_pitcher])

# * Step 7. Aggregate into one DF
four_week_pitcher_aggregate = aggregate_pitcherpreformance(pitchers_df, home_pitcher)
game_info['homeP_xBA_4weeks'] = four_week_pitcher_aggregate.loc[four_week_pitcher_aggregate['home_away'] == 'home'].estimated_ba_using_speedangle.values[0]
game_info['awayP_xBA_4weeks'] = four_week_pitcher_aggregate.loc[four_week_pitcher_aggregate['home_away'] == 'away'].estimated_ba_using_speedangle.values[0]

# * Step 8. Batting Information now
home_batters, away_batters = identify_home_away_batters(full_game_df)

# * Step 9. Last four weeks for batters
home_batters_preform, away_batters_preform = batter_lastfourweeks(game_day, 28, home_batters, away_batters)

# * Step 10. Get top 9 batters
home_top9, away_top9 = get_top9batters(home_batters_preform), get_top9batters(away_batters_preform)

# * Step 11. Aggregate
home_last4weeks = aggregate_batterpreformance(home_batters_preform, only_top9=True)
home_last4weeks['home_away'] = 'home'
home_last4weeks['rank'] = home_last4weeks['estimated_ba_using_speedangle'].rank(ascending=False, method='first').astype(int)
home_last4weeks['ha_rank'] = home_last4weeks['home_away'] + home_last4weeks['rank'].astype(str)
home_last4weeks['game_date'] = game_day
home_batting_4_weeks = home_last4weeks.pivot(index='game_date', columns = 'ha_rank', values='estimated_ba_using_speedangle')

away_last4weeks = aggregate_batterpreformance(away_batters_preform, only_top9=True)
away_last4weeks['home_away'] = 'away'
away_last4weeks['rank'] = away_last4weeks['estimated_ba_using_speedangle'].rank(ascending=False, method='first').astype(int)
away_last4weeks['ha_rank'] = away_last4weeks['home_away'] + away_last4weeks['rank'].astype(str)
away_last4weeks['game_date'] = game_day
away_batting_4_weeks = away_last4weeks.pivot(index='game_date', columns = 'ha_rank', values='estimated_ba_using_speedangle')

all_batting = home_batting_4_weeks.merge(away_batting_4_weeks, on='game_date', how='inner')

# * Step 12. Join back to game info
all_batting.index = pd.to_datetime(all_batting.index)
game_info = game_info.merge(all_batting, on='game_date', how='inner')

# * Step 13. Join back Results
game_info