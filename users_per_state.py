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
pages of users paginated list and adds named user to the usr_list
return: usr_list
   
"""

  
def get_user_by_location(usrs_list, usrs):
    page_number = 0
    count = 0
    total_users = usrs.totalCount
    try:
        while(count <= total_users):
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
  


#Reads the maximum_repo_state pickle
with open('pickles/maximum_repo_state.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f)

'''
maximum_repo_state = {'Nevada': 200, 'New Hampshire': 51, 'New Jersey': 51, 'New Mexico': 51, 'New York': 401, 'North Carolina': 101, 'North Dakota': 51, 'Ohio': 751, 'Oklahoma': 251, 'Oregon': 751, 'Pennsylvania': 451, 'Rhode Island': 51, 'South Carolina': 51, 'South Dakota': 151, 'Tennessee': 551, 'Texas': 1951, 'Utah': 551, 'Vermont': 701, 'Virginia': 1701, 'Washington': 801, 'West Virginia': 51, 'Wisconsin': 351, 'Wyoming': 401}


#Gets users of all locations from the maximum_repo_state

"""
Goes thorugh all the items in the maximum_repo_state dictionary.
Uses key as a location and value as the maximum repo to iterate through.
It searches users with specific repos (which increases by 1, and goes until maximum repo) and for a specific location(key)
It uses get_user_by_location to get users for that location and specific repo number, and returns user_list
At the end, it appends the location, users into the github_data_dict and pickles it

"""
'''

github_data_dict = {}

for key, value in maximum_repo_state.items():
    print("key: {} & value: {}".format(key, value))
    users_list = []
    repos = 1
    state = key
    year = 2007
    more_than_1000 = False                                      
    users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))                        #gets all the users for a number of repos and location
    print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))
    
    #As github only allow 1000 results per search, a condition to check if its users.totalCount == 1000
    #if it is, then adds dates constraints to narrow the searches
    if(users.totalCount == 1000):
        users =  client.search_users(query= 'created:{}-01-01..{}-01-01 repos:{} location:{}'.format(year,(year+1), repos, state ))
        print("State {} & repos: {} & from {} to {}  & number of users {}".format(state, repos, year, (year+1), users.totalCount))
        more_than_1000 = True
        
    while(repos <= value ):
        users_list = get_user_by_location(users_list, users)
        print("length of users_list", len(users_list))
        print("----------------------next--------------------------------")
        if(more_than_1000 == True):
            while(year < 2020):
                year += 1
                users =  client.search_users(query= 'created:{}-01-01..{}-01-01 repos:{} location:{}'.format(year,(year+1), repos, state ))
                print("State {} & repos: {} & from {} to {}  & number of users {}".format(state, repos, year, (year+1), users.totalCount))
                users_list = get_user_by_location(users_list, users)
                print("length of users_list", len(users_list))
                print("----------------------next--------------------------------")
        
        more_than_1000 = False
        year = 2007
        repos += 1
        users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))
        print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))
        time.sleep(3)
        if(users.totalCount == 1000):
            users =  client.search_users(query= 'created:{}-01-01..{}-01-01 repos:{} location:{}'.format(year,(year+1), repos, state ))
            print("State {} & repos: {} & from {} to {}  & number of users {}".format(state, repos, year, (year+1), users.totalCount))
            more_than_1000 = True
    
    print(users_list)    
    github_data_dict[key] = users_list
    
    #pickleing the maximum_repo_state dictionary 
    print("--------------Now pickling-------------------------------------")
    with open('pickles/users_pickles/{}.pkl'.format(key), 'wb') as f:
        pickle.dump(github_data_dict, f)













'''
with open('pickles/users_pickles/Arkansas.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f)  
array = maximum_repo_state.get('Arkansas')      
print(array)
import collections
print([item for item, count in collections.Counter(array).items() if count > 1])

print(len(set(array)))




















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


