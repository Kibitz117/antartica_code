import dearpygui.dearpygui as dpg
from bs4 import BeautifulSoup
import requests
import pandas as pd
#Class thet creates a user object with a GitHub username and file location to download the user's repositories
class GitHubUser:
    def __init__(self, name, location):
        self.name = name
        self.location = location
    def getUserData(self):
        return self.name, self.location
    def setUserData(self, name, location):
        self.name = name
        self.location = location
#Function that takes in a user object and returns the user's repositories
def getGitHub(user):
    userData = user.getUserData()
    username = userData[0]
    location = userData[1]
    url = "https://api.github.com/users/" + username
    print(url)
    response = requests.get(url)
    data = response.json()
    return data['repos_url']
#Function that scrapes github for all user respositories and puts them in a list
def scrapeGitHub(site):
    response = requests.get(site)
    data = response.json()
    repos = []
    for repo in data:
        repos.append(repo['name'])
    return repos
#Function that creates an excel file with the user's repositories
def createExcelFile(user,repos,location):
    df = pd.DataFrame(columns=['Repository Name'])
    for repo in repos:
        df = df.append({'Repository Name': repo}, ignore_index=True)
    df.to_excel(f'{location}/{user.name}.xlsx', index=False)
    return df
#Function that saves input in a GUI and runs the functions to create the excel file
def save_data(sender,data,user_data):
    user=GitHubUser(dpg.get_value(user_data[0]),dpg.get_value(user_data[1]))
    data=getGitHub(user)
    repos=scrapeGitHub(data)
    createExcelFile(user,repos,user.location)
    return user
#The following code creates the dearpygui window and creates a form for someone to fill out with a GitHub username and file location
dpg.create_context()
dpg.create_viewport(width=600, height=200)
dpg.setup_dearpygui()
user=[]
with dpg.window(label="Welcome to Antartica",width=600, height=200):
    username=dpg.add_input_text(label="GitHub Username")

    location=dpg.add_input_text(label="File Location")
    dpg.add_button(label="Save",callback=save_data,user_data=[username,location])
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
