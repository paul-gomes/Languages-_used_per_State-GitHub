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

def get_all_repos(repos, repo_list):
    page_number = 0
    count = 0
    total_repos = repos.totalCount
    try:
        while(count <= total_repos):
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
            
            

with open('pickles/users_pickles/Alabama.pkl', 'rb') as f:
    maximum_repo_state  = pickle.load(f) 
    
users = maximum_repo_state.get('Alabama')
users.reverse()   
print(len(users))

languages = {}

f = open("demofile2.txt", "a")
for user in users:
    print("user", user)
    repo_list = []
    repos = client.get_user(user.login).get_repos('all')
    repo_list = get_all_repos(repos, repo_list)
    print("repo_list", repo_list)
    for repo in repo_list:
        language = repo.get_languages()
        f.write(repo, "---", languages, "\n")
        print("language", language)
        for key, value in language.items():
            if key in languages:
                languages[key] = languages.get(key) + value
            else:
                languages[key] = value
        
        print("Languages", languages)
    
  
    
    
    
    
'''
print(users[1])
repo_list = []
repos = client.get_user(users[3].login).get_repos('all')
repo_list = get_all_repos(repos, repo_list)
print(repo_list)
languages = repo_list[0].get_languages()
print(languages)
'''

