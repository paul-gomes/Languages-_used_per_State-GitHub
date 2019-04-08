# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 08:07:40 2019
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
Goal: function that gets all the repositories for a specific user.
Function takes repo_list and repo as parameter and goes thorugh different 
pages of repos paginated list and adds repos to the repo_list
return: repo_list
   
"""

def get_all_repos(repo_list, repos):
    page_number = 0
    count = 0
    total_repos = repos.totalCount
    try:
        while(count <= total_repos):
            time.sleep(6)
            repos_per_page = repos.get_page(page_number)
            if len(repos_per_page) == 0: return repo_list
            repo_list.extend(repos_per_page)
            count += len(repos_per_page)
            page_number += 1
            print("page number", page_number)
            print("count", count)
        return repo_list
    except Exception as e:
        print(str(e))
        return repo_list
            

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']           

#reads the state pickle and saves it to maximum_repo_state, which is a dictionary
with open('pickles/users_pickles/Alabama.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f) 
    
#Gets users list for a specific state, which is a key of the dictionary
users = maximum_repo_state.get('Alabama')

users.reverse()   
print(len(users))

languages = {}

#f = open("checks_language_calculations/language_data.txt", "a")
for user in users:
    print("user", user)
    repo_list = []
    repos = client.get_user(user.login).get_repos('all')
    repo_list = get_all_repos(repos, repo_list)
    print("repo_list", repo_list)
    for repo in repo_list:
        time.sleep(2)
        language = repo.get_languages()
        #f.write("{},".format(language))
        print("language", language)
        for key, value in language.items():
            if key in languages:
                languages[key] = languages.get(key) + value
            else:
                languages[key] = value
        
        print("Languages", languages)
    
  
    
    
    

