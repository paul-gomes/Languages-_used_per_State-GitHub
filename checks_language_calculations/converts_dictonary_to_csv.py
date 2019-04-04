# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 00:21:26 2019
@author: Anik Paul Gomes
"""


"""
This script reads text file which contains list of dictonary and converts into 
csv file. So that validity of the calculations can be checked in excel for shorter
amount of data

"""

#Added square brackets in the beginning and at the end of the text file to make it 
#list of dictionaries before converting into csv.
 
from pathlib import Path
import pandas as pd
import ast


#Reads text file into toCSV  using pathlib module
toCSV = Path('language_data.txt').read_text()

#Converts string representation of dictionary into dictionary
toCSV = ast.literal_eval(toCSV)

#Converts dictionary into data frame
data = pd.DataFrame(toCSV)

#dataframe to csv
data.to_csv('language_data.csv')
