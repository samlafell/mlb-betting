from numpy import column_stack
import pandas as pd

data = pd.read_csv('Data/GL2021.TXT', 
                   sep=",", 
                   header=None)

columns = ['Date', 'Game_Type', 'Day_Week', 'Visitors_Name',
           'V_League', 'V_GameNum', 'Home_Name',
           'H_League', 'H_GameNum', 'V_Score', 'H_Score',
           'Total_Outs_in_Game', 'Day_Night', 'Completion_Info', 
           'Forfeit_Info', 'Protest_Info', 'Park_ID', 'Attendance',
           'Time_Minutes', 'V_LineScore', 'Home_LineScore',
           'V_AtBats', 'V_Hits', 'V_Doubles', 'V_Triples', 'V_HR', 'V_RBI', 
           'V_SacHit', 'V_SacFlies', 'V_HBP', 'V_Walks', 'V_IW', 'V_K', 'V_SB',
           'V_CS', 'V_GIDP', 'V_CatchInteference', 'V_LOB',
           'V_PitchersUsed', 'V_Individal_ER', 'V_Team_ER', 'V_WP', 'V_Balks',
           'V_Putouts', 'V_Assists', 'V_Errors', 'V_PassedBalls', 'V_DP', 'V_TP',
           'H_AtBats', 'H_Hits', 'H_Doubles', 'H_Triples', 'H_HR', 'H_RBI', 
           'H_SacHit', 'H_SacFlies', 'H_HBP', 'H_Walks', 'H_IW', 'H_K', 'H_SB',
           'H_CS', 'H_GIDP', 'H_CatchInteference', 'H_LOB',
           'H_PitchersUsed', 'H_IndiHidal_ER', 'H_Team_ER', 'H_WP', 'H_Balks',
           'H_Putouts', 'H_Assists', 'H_Errors', 'H_PassedBalls', 'H_DP', 'H_TP',
           'HP_UmpireID', 'HP_Umpire_Name', '1B_UmpireID', '1B_UmpireName',
           '2B_UmpireID', '2B_UmpireName', '3B_UmpireID', '3B_UmpireName',
           'LF_UmpireID', 'LF_UmpireName', 'RF_UmpireID', 'RF_UmpireName',
           'V_ManagerID', 'V_ManagerName', 'H_ManagerID', 'H_ManagerName',
           'WP_ID', 'WP_Name', 'LP_ID', 'LP_Name', 'Closer_ID', 'Closer_Name',
           'GameWinningRBI_ID', 'GameWinningRBI_Name', 
           'V_SP_ID', 'V_SP_Name', 'H_SP_ID', 'H_SP_Name', 
           'V_1stBat_ID', 'V_1stBat_Name', 'V_1stBat_Position',
           'V_2ndBat_ID', 'V_2ndBat_Name', 'V_2ndBat_Position',
           'V_3rdBat_ID', 'V_3rdBat_Name', 'V_3rdBat_Position',
           'V_4thBat_ID', 'V_4thBat_Name', 'V_4thBat_Position',
           'V_5thBat_ID', 'V_5thBat_Name', 'V_5thBat_Position',
           'V_6thBat_ID', 'V_6thBat_Name', 'V_6thBat_Position',
           'V_7thBat_ID', 'V_7thBat_Name', 'V_7thBat_Position',
           'V_8thBat_ID', 'V_8thBat_Name', 'V_8thBat_Position',
           'V_9thBat_ID', 'V_9thBat_Name', 'V_9thBat_Position',
           'H_1stBat_ID', 'H_1stBat_Name', 'H_1stBat_Position',
           'H_2ndBat_ID', 'H_2ndBat_Name', 'H_2ndBat_Position',
           'H_3rdBat_ID', 'H_3rdBat_Name', 'H_3rdBat_Position',
           'H_4thBat_ID', 'H_4thBat_Name', 'H_4thBat_Position',
           'H_5thBat_ID', 'H_5thBat_Name', 'H_5thBat_Position',
           'H_6thBat_ID', 'H_6thBat_Name', 'H_6thBat_Position',
           'H_7thBat_ID', 'H_7thBat_Name', 'H_7thBat_Position',
           'H_8thBat_ID', 'H_8thBat_Name', 'H_8thBat_Position',
           'H_9thBat_ID', 'H_9thBat_Name', 'H_9thBat_Position',
           'Additional_Info',
           'Acquisition_Information']
           

columns_abbreviated = data.iloc[:10, 0:len(columns)]
columns_abbreviated.columns = columns
columns_abbreviated