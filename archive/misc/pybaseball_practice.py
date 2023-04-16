import pandas as pd
import pybaseball as pb
pd.set_option('display.max_columns', 15)

######### Get Team Performance for a Season ##########

cubs2021_batting = pb.team_game_logs(2021, 'CHC', 'batting')
cubs2021_pitching = pb.team_game_logs(2021, 'CHC', 'pitching')
cubs2021_pitching

########## Get Statcast Pitching Performance #############
jonlester_game_log = cubs2021_batting.iloc[-2,-1]
jlester = pb.playerid_lookup('lester', 'jon')
jlester

pb.statcast_pitcher(start_dt='2021-06-24', end_dt='2021-09-27', player_id=jlester['key_mlbam'].values[0])