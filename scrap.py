from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient
from collections import defaultdict

playerDataList = []
player_ratings = {"trait": "", "num": ""}

player_info= {"name": "","position": "","team": "", "height":"", "weight":"", "picture": "", "ratings": []}
player_links = ["https://www.maddenratings.com/tyler-lockett", "https://www.maddenratings.com/tom-brady", "https://www.maddenratings.com/von-miller"]
ratings_list = []
ratings = {"trait": "","num": ""}
player_page = requests.get("https://www.maddenratings.com/tyler-lockett").text

for i in range(2):

    soup = BeautifulSoup(player_links[i], 'html.parser')
    page = soup.find("div", class_="tab-content mb-4 pb-2").text
    name = soup.find("h1", class_="header-title pt-2 mb-0").text.lstrip()
    print(name)
    playerInfo = soup.find("div", class_="header-subtitle")

# print(team)
    player_info["name"] = name
    # print(player_info)
for i in range(7):
    data = page.select("ul")[i]

    for li in data.find_all("li"):
        ratings = li.text
        split_ratings = ratings.split(" ", 1)

        player_ratings["num"] = int(split_ratings[0])
        player_ratings["trait"] = split_ratings[1]
        ratings_list.append(player_ratings)
        # print(ratings_list)
        player_info["ratings"] = ratings_list



urlName = name.replace(" ", "-")
nflUrl = "https://www.nfl.com/players/" + urlName
nfl_page = requests.get(nflUrl).text
nfl_soup = BeautifulSoup(nfl_page, 'html.parser')
nflPicture = nfl_soup.find("img")["data-src"]
nflPosition = nfl_soup.find("span", class_="nfl-c-player-header__position").text
player_info["picture"] = nflPicture
player_info["position"] = nflPosition
nflPlayerTeam = nfl_soup.find("a", class_="nfl-o-cta--link").text
player_info["team"] = nflPlayerTeam
# nflPlayerHT = nfl_soup.find("div", class_="nfl-c-player-info__value").text
# player_info["height"] = nflPlayerHT
nflPlayerWT = nfl_soup.find("div", class_="nfl-c-player-info__value").text

nflInfobox = nfl_soup.find("div", class_="d3-l-col__col-12 nfl-c-player-info__content")
# print(nflInfobox)
heightWeight = []
for i in range(2):
    info = nflInfobox.select("li")[i]
    htwt = info.text
    htwt2 = htwt.split()
    heightWeight.append(htwt)
player_info["weight"] = int(heightWeight[1].split("t")[1])
heightFT = heightWeight[0].split("t")[1]
playerHeight = heightFT.split("-")
playerHtIn= (int(playerHeight[0])*12) + int(playerHeight[1])
player_info["height"] = playerHtIn
# print(nflPlayerWT)
# print(type(player_info["ratings"]))

import pymongo



# print(player_info)
json_obj = json.dumps(player_info)
# print(json_obj)
with open(player_info["name"]+".json", "w") as outfile:
    outfile.write(json_obj)




----------------------------------------------------------------------------------------------


from bs4 import BeautifulSoup
import requests

# get team links ->
team_link_source = requests.get("https://www.maddenratings.com/teams")
soup = BeautifulSoup(team_link_source.text, 'html.parser')
team_links = []
teams = soup.find_all("div", class_="card-body pt-3 ml-n2 pl-0 pr-2")
for div in teams:
    team_links.append(div.a["href"])
print(team_links)


players = []
player_link_list = []
ratings = {"trait": "", "rating": ""}
# for link in team_links:
#     sauce = requests.get(link).text
#     soup = BeautifulSoup(sauce, 'html.parser')
#     players = soup.find_all("div", class_="entries")
#     for links in players:
#
#         player_link = links.find("a")['href']
#         if "madden" in player_link:
#             player_link_list.append(player_link)
# print(player_link_list)
#
# ratings_list = []
#
# player_page = requests.get("https://www.maddenratings.com/tyler-lockett").text
# new_soup = BeautifulSoup(player_page, 'html.parser')
# page = new_soup.find("div", class_="tab-content mb-4 pb-2").text
# # name = page.find("h1", class_="header-title pt-2 mb-0")
#
#
#
#
#
# player_ratings = {"trait": "", "num": ""}
#
# player_info: {"name": "", "ratings": []}
#
# # complete section
# for i in range(7):
#     data = page.select("ul")[i]
#     player_info["name"]
#     for li in data.find_all("li"):
#         ratings = li.text
#         split_ratings = ratings.split(" ", 1)
#
#         player_ratings["num"] = split_ratings[0]
#         player_ratings["trait"] = split_ratings[1]
#         print(player_ratings)
#
#
# # get player traits ->
# ratings_list = []
# ratings = {"trait": "","num": ""}
# player_page = requests.get("https://www.maddenratings.com/tyler-lockett").text
# new_soup = BeautifulSoup(player_page, 'html.parser')
# # page = new_soup.find("div", class_="main")
# name = new_soup.find("h1").text.lstrip()
#
#
# # nfl page scrape -> complete
# urlName = name.replace(" ", "-")
# nflUrl = "https://www.nfl.com/players/" + urlName
# nfl_page = requests.get(nflUrl).text
# nfl_soup = BeautifulSoup(nfl_page, 'html.parser')
# nflPicture = nfl_soup.find("img")["data-src"]
#
#
# # wiki scrape ->
# wikiUrl = "https://en.wikipedia.org/wiki/" + urlName
# wiki_page = requests.get(wikiUrl).text
# infoBox = wiki_page.find("td", class_="infobox-data")
#
# print(infoBox)
#
# # ------------------------------>
# # get team links ->
# team_link_source = requests.get("https://www.maddenratings.com/teams")
# soup = BeautifulSoup(team_link_source.text, 'html.parser')
# team_links = []
# teams = soup.find_all("div", class_="card-body pt-3 ml-n2 pl-0 pr-2")
# for div in teams:
#     team_links.append(div.a["href"])
# # print(team_links)
# # get individual player links from each team ->
# player_link_list = []
# ratings = {"trait": "", "rating": ""}
# for link in team_links:
#     sauce = requests.get(link).text
#     soup = BeautifulSoup(sauce, 'html.parser')
#     players = soup.find_all("div", class_="entries")
#     for links in players:
#         player_link = links.find("a")['href']
#         if "madden" in player_link:
#             player_link_list.append(player_link)
# # print(player_link_list)
# # # get madden traits ->
# for playerLinks in player_link_list:
#     playerPage = requests.get(playerLinks).text
#     soup = BeautifulSoup(playerPage, 'html.parser')
#     # page = playerPage.find("div", class_="tab-content mb-4 pb-2").text
#     names = soup.find("h1").text.lstrip()
#     # print(names)
#     for i in range(7):
#         data = page.select("ul")[i]
#         for li in data.find_all("li"):
#             ratings = li.text
#             split_ratings = ratings.split(" ", 1)
#
#             player_ratings["num"] = split_ratings[0]
#             player_ratings["trait"] = split_ratings[1]
#             playerData["madden_ratings"] = player_ratings
# #
# # print(playerData)

# playerDataList = []
# player_ratings = {"trait": "", "num": ""}
# player_info= {"name": "","position": "","team": "", "height":"", "weight":"", "picture": "", "ratings": []}
# player_links = ["https://www.maddenratings.com/tyler-lockett", "https://www.maddenratings.com/tom-brady", "https://www.maddenratings.com/von-miller"]
# for links in player_links:
#     soup = BeautifulSoup(links, 'html.parser')
#     page = soup.find("div", class_="tab-content mb-4 pb-2")
#     name = soup.find("h1")
#     print(name)
