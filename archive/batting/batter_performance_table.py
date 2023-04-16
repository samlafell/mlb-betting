'''
Title: Batter Performance Table
Author: Sam LaFell
Date: 11/5/2022
Purpose: I got a little carried away on my last notebook. Time to optimize some code.

Granularity: xBA by pitch for each batter. By pitcher handiness.
'''

# Import Libraries
import pandas as pd
import pybaseball as pb
import os
import numpy as np
import re

# Pick one specific game
from pybaseball import statcast_single_game
data = statcast_single_game(529429)

# Statcast
from pybaseball import statcast
data = statcast('2018-03-30', '2018-03-30')
data.columns

# BWAR
from pybaseball import bwar_bat
# get war stats from baseball reference 
data = bwar_bat()
# get war stats plus additional fields from this table 
data = bwar_bat(return_all=True)