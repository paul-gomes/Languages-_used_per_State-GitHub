# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:27:58 2019
@author: Anik Paul Gomes

"""

from github import Github
import time
import pickle
import csv

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
Goal: function that gets all the unique user for a specific state
Function takes users_set and users as parameter and goes thorugh different 
pages of users paginated list and adds unique named user to the user_set set
return: user_set
    
"""



def get_user_by_location(usrs_set, usrs):
    page_number = 0
    count = 0
    try:
        while(count <= usrs.totalCount):
            time.sleep(6)
            page = usrs.get_page(page_number)
            if len(page) == 0: return usrs_set
            for usr in page:
                usrs_set.add(usr)
            count += len(page)
            page_number += 1
            print("page number", page_number)
            print("count", count)
        return usrs_set
    
    except Exception as e:
        print(str(e))
        return usrs_set
    
    
    
    


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
Locations have both full state name as well ass abbreviation because "why Github?"
Search by full state name and abbrev give different results

"""


'''
maximum_repo_state  = {}


for key, value in us_state_abbrev.items():
    maximum_repo_state[key] = maximum_repos(key)
    maximum_repo_state[value] = maximum_repos(value)
    


print(maximum_repo_state)


#pickleing the maximum_repo_state dictionary 
with open('maximum_repo_state.pkl', 'wb') as f:
    pickle.dump(maximum_repo_state, f)
'''



#Reads the maximum_repo_state pickle
with open('maximum_repo_state.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f)



#Gets users of all locations from the maximum_repo_state


#Writes the header of the csv file which stores the location, all the named users, number of users
with open('github_users_by_state.csv', 'a', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["Location", "Users", "Number of users"])

csvFile.close()



"""
Goes thorugh all the items in the maximum_repo_state dictionary.
Uses key as a location and value as the maximum repo to iterate through.
It searches users with specific repos (which increases by 1, and goes until maximum repo) and for a specific location
It uses get_user_by_location to get uniques users for that location and specific repo number, and returns user_set
Eventually, appends the location, users, number of users into the csv.

"""


for key, value in maximum_repo_state.items():
    print("key: {} & value: {}".format(key, value))
    users_set= set()
    repos = 1
    state = key
    users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))
    print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))

    while(repos <= value ):
        users_set = get_user_by_location(users_set, users)
        print("length of users set", len(users_set))
        print("----------------------next--------------------------------")
        repos += 1
        users =  client.search_users(query= 'repos:{} location:{}'.format(repos, state ))
        print("State {} & repos: {} & number of users {}".format(state, repos, users.totalCount))
    
    print(users_set)
    with open('github_users_by_state.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([key, users_set, len(users_set)])
    csvFile.close()



    






















''' 
mo_users= set()
mo = client.search_users(query= 'repos:>1 location:MO')
repo_count = 1        
while(mo.totalCount > 0):
    time.sleep(6)
    print("Greater than {} repos & users {}".format(repo_count, mo.totalCount))
    repo_count += 50
    mo = client.search_users(query= 'repos:>{} location:MO'.format(repo_count))
    
print(repo_count)
#print(mo.get_page(40))
#print(usa.get_page(0))
#mo_page = mo.get_page(0)
#mo_users.add(set(mo_page))

  

count = 0
while(count < 3):
    page = mo.get_page(count)
    for x in page:
        mo_users.add(x)
    #time.sleep(6)
    print("count", count)
    count += 1
    
#print(mo_users)
print(len(mo_users))



try:
    while(True):
        page = usa.get_page(count)
        for x in page:
            usa_users.append(x)
        time.sleep(6)
        print("count", count)
        count += 1
       
except Exception as e:
     print("done")
     print(count)
     print(usa_users)
     print("List length", len(usa_users))
     print(str(e))
     
     
     
     
     

'''

