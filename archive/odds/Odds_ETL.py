import os  
import pandas as pd
import numpy as np


'''
TO DO:
- Add Comments
- Chicago Cubs show as "CHC" and also "CUB" in the data, need to fix that.
'''


df2 = pd.DataFrame()
path = '/Users/samlafell/Desktop/sports_betting_project/data/external/odds_files/'
for file_year in list(range(2017,2023)):
    df_year = pd.read_excel(os.path.join(path, f'mlb_odds_{file_year}.xlsx'))
    df_year['Date'] = df_year.Date.astype(str)
    df_year['Date'] = df_year['Date'] + str(file_year)
    df_year["Date"] = pd.to_datetime(df_year["Date"], format='%m%d%Y')
    
    if 'OpenOU' in df_year.columns:
        df_year.rename(columns = {'OpenOU':'Open OU', 'CloseOU':'Close OU', 'RunLine':'Run Line'}, inplace=True)
    
    # Concat to bigger df
    df2 = pd.concat([df2, df_year], ignore_index=True)
    
df2.drop_duplicates(inplace=True)

# How many unique games were played?
loop_to = int(df2.shape[0]/2)

# Create a list of these numbers to get Game IDs
lis = list(range(loop_to))

# Two rows per game, repeat each value 2 times
gameid = np.repeat(lis, 2)

# Add as a column
df2['Game_ID'] = gameid

# Neutral Game? Otherwise we can't pivot because of repeating "N" in "VH" column
df2['Neutral_Game'] = np.where(df2['VH'] == 'N',
                               1,
                               0)

neutral_games = df2.groupby(['Date', 'Game_ID', 'VH']).filter(lambda x: x['Team'].count() > 1)
neutral_games['VH'] = ['V', 'H']*(neutral_games['Game_ID'].nunique())
df2.loc[df2.index.isin(neutral_games.index), ['VH']] = neutral_games['VH']


df2_wide = pd.pivot(df2, index = 'Game_ID', columns = 'VH', values= ['Date', 'Team', 'Final', 'Open', 'Close', 'Run Line', 'Open OU', 'Close OU', 'Neutral_Game'])
prefixes = [col[1] for col in df2_wide.columns]
df2_wide = df2_wide.droplevel(1, axis = 1)
df2_wide.columns = prefixes + df2_wide.columns
df2_wide.drop(['VDate', 'VClose OU', 'VOpen OU', 'VNeutral_Game'], axis = 1, inplace = True)
df2_wide.rename(columns = {'HDate': 'Date',
                 'HOpen OU': 'Open_OU',
                 'HClose OU': 'Close_OU',
                 'HNeutral_Game': 'Neutral_Game'},
                inplace = True)

df2_wide['Winner'] = np.where(df2_wide['HFinal'] > df2_wide['VFinal'],
                              df2_wide['HTeam'],
                              df2_wide['VTeam'])

df2_wide['OverUnder'] = np.where(df2_wide['HFinal'] + df2_wide['VFinal'] > df2_wide['Close_OU'],
                                 'Over',
                                 np.where(df2_wide['HFinal'] + df2_wide['VFinal'] == df2_wide['Close_OU'],
                                          'Push',
                                          'Under'))

interim_data = '/Users/samlafell/Documents/Learning/sports_betting_project/data/interim'
df2_wide.to_csv(os.path.join(interim_data, 'matchups_and_odds_2017-2022.csv'))