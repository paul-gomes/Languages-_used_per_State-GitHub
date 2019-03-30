# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:27:58 2019
@author: Anik Paul Gomes

"""

from github import Github
import time
import pickle

#Reads access token from a file
f = open("access_token.txt", "r")
access_token = f.read()


#Creates github instance
client = Github(access_token)

"""
Goal: finds maximum repos a user has for a specific location.
Functions takes location parameter and finds the maximum number of repositories
a user of that location has. 
return: count of maximum repo

"""

def maximum_repos(location):
    users = client.search_users(query= 'repos:>1 location:{}'.format(location))
    repo_count = 0        
    while(users.totalCount > 0):
        time.sleep(6)
        print("Location: {} Greater than {} repos & users {}".format(location, repo_count, users.totalCount))
        repo_count += 50
        users = client.search_users(query= 'repos:>{} location:{}'.format(repo_count, location))
    return repo_count
    



"""
Goal: function that gets all the users for a specific state
Function takes usrs_list and usrs as parameter and goes thorugh different 
pages of users paginated list and adds named user to the usr_list set
return: usr_list
    
"""



def get_user_by_location(usrs_list, usrs):
    page_number = 0
    count = 0
    try:
        while(count <= usrs.totalCount):
            time.sleep(6)
            usrs_per_page = usrs.get_page(page_number)
            if len(usrs_per_page) == 0: return usrs_list
            usrs_list.extend(usrs_per_page)
            count += len(usrs_per_page)
            page_number += 1
            print("page number", page_number)
            print("count", count)
        return usrs_list
    
    except Exception as e:
        print(str(e))
        return usrs_list
    
    
    
    


#Dictionary: Names of US states with abbreviations 
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',         
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


"""
Dictionary: To save the maximum number repos of a user for a specific location 
Dictionary : Key= location, values= maximum_repos
Locations have both full state name as well as abbreviation because "why Github?"
Search by full state name and abbrev give different results. 

Changed by mind later. Only seraching by full state name as searching by state abbrev 
gives users from different country for some state abbrev.

"""


'''
maximum_repo_state  = {}


for key, value in us_state_abbrev.items():
    maximum_repo_state[key] = maximum_repos(key)
    
    #Even though searching with state code gives more and different users, for some state
    #it gives users from different country. So just to avoid unwanted data, i will only search
    #with full state and comment out the search by State abbrev. Less data but correct.
    
    #maximum_repo_state[value] = maximum_repos(value)
    


print(maximum_repo_state)


#pickleing the maximum_repo_state dictionary 
with open('pickles/maximum_repo_state.pkl', 'wb') as f:
    pickle.dump(maximum_repo_state, f)
'''  




#Reads the maximum_repo_state pickle
with open('pickles/maximum_repo_state.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f)

print(maximum_repo_state)
print(len(maximum_repo_state))



#maximum_repo_state = {'Florida': 901, 'FL': 751, 'Georgia': 501, 'GA': 551, 'Hawaii': 201, 'HI': 301, 'Idaho': 401, 'ID': 251, 'Illinois': 501, 'IL': 1551, 'Indiana': 251, 'IN': 33601, 'Iowa': 451, 'IA': 501, 'Kansas': 401, 'KS': 1201, 'Kentucky': 301, 'KY': 401, 'Louisiana': 1851, 'LA': 20301, 'Maine': 551, 'ME': 251, 'Maryland': 501, 'MD': 1101, 'Massachusetts': 1151, 'MA': 1801, 'Michigan': 551, 'MI': 3951, 'Minnesota': 1001, 'MN': 551, 'Mississippi': 351, 'MS': 201, 'Missouri': 501, 'MO': 1901, 'Montana': 251, 'MT': 401, 'Nebraska': 351, 'NE': 951, 'Nevada': 11751, 'NV': 1301, 'New Hampshire': 51, 'NH': 1051, 'New Jersey': 51, 'NJ': 1251, 'New Mexico': 51, 'NM': 1001, 'New York': 401, 'NY': 15701, 'North Carolina': 101, 'NC': 1451, 'North Dakota': 51, 'ND': 451, 'Ohio': 751, 'OH': 901, 'Oklahoma': 251, 'OK': 251, 'Oregon': 751, 'OR': 751, 'Pennsylvania': 451, 'PA': 501, 'Rhode Island': 51, 'RI': 551, 'South Carolina': 51, 'SC': 1351, 'South Dakota': 151, 'SD': 401, 'Tennessee': 551, 'TN': 801, 'Texas': 1951, 'TX': 2951, 'Utah': 551, 'UT': 1101, 'Vermont': 701, 'VT': 251, 'Virginia': 1701, 'VA': 1351, 'Washington': 801, 'WA': 2351, 'West Virginia': 51, 'WV': 501, 'Wisconsin': 351, 'WI': 851, 'Wyoming': 401, 'WY': 251}


#maximum_repo_state = {'Delaware': 251, 'DE': 20301}



#Gets users of all locations from the maximum_repo_state

"""
Goes thorugh all the items in the maximum_repo_state dictionary.
Uses key as a location and value as the maximum repo to iterate through.
It searches users with specific repos (which increases by 1, and goes until maximum repo) and for a specific location(key)
It uses get_user_by_location to get users for that location and specific repo number, and returns user_list
At the end, it appends the location, users, number of users into the github_data_dict and pickles it

"""
'''

github_data_dict = {}

for key, value in maximum_repo_state.items():
    print("key: {} & value: {}".format(key, value))
    users_list = []
    repos = 1
    state = key
    users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))
    print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))

    while(repos <= value ):
        users_list = get_user_by_location(users_list, users)
        print("length of users_list", len(users_list))
        print("----------------------next--------------------------------")
        repos += 1
        users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))
        print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))
    
    print(users_list)
    
    github_data_dict[key] = users_list
    
    
#pickleing the maximum_repo_state dictionary 
with open('pickles/{}.pkl'.format(key), 'wb') as f:
    pickle.dump(github_data_dict, f)














with open('pickles/users_pickles/alabama.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f)

print(len(maximum_repo_state.get('AL')))

'''
















"""
#Writes the header of the csv file which stores the location, all the named users, number of users
with open('data/github_users_by_state.csv', 'a', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["Location", "Users", "Number of users"])

csvFile.close()

    
    with open('data/github_users_by_state.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([key, users_list, len(users_list)])
    csvFile.close()


"""


