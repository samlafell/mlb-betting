position_dict = {
 'P': 1,
 'C': 2,
 '1B': 3,
 '2B': 4,
 '3B': 5,
 'SS': 6,
 'LF': 7,
 'CF': 8,
 'RF': 9,
 'DH': 10
}

# What about position?
from pybaseball import fielding_leaders
fielding_df = fielding_leaders.fg_fielding_data(start_season = 2019, end_season = 2023, split_seasons = 1)[['IDfg', 'Season', 'Name', 'Team', 'Pos', 'G', 'GS']]
fielding_df[['First Name', 'Last Name']] = fielding_df['Name'].str.split(' ', n=1, expand=True)
fielding_df['Rank'] = fielding_df.groupby(['Season', 'Team', 'Pos'])['GS'].rank(ascending=False, method='dense')
fielding_df['Pos_ID'] = fielding_df['Pos'].map(position_dict)


# Now find them
from pybaseball import playerid_reverse_lookup

playerid_reverse_lookup(fielding_df['IDfg'], 'fangraphs')



player_id_df = pd.DataFrame()
for i in range(len(fielding_df)):
    last_name = fielding_df.iloc[i, [-4,-3]].values[1]
    first_name = fielding_df.iloc[i, [-4,-3]].values[0]
    player_id_lookup = playerid_lookup(last = last_name, first = first_name)
    player_id_df = pd.concat([player_id_df, player_id_lookup])

from pybaseball import playerid_lookup
playerid_lookup(last = 'Harper', first = 'Bryce')





import pybaseball
from pybaseball import statcast
pybaseball.cache.enable()
#df = statcast(start_dt = '2018-03-01', end_dt = '2023-04-15', parallel = True)[['batter', 'pitcher']]

batters_big = pybaseball.statcast_batter(start_dt='2018-03-01', end_dt = '2023-04-15')