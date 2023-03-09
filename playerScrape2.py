import itertools

from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient

player_ratings = {"trait": "", "num": ""}
madden_ratings = {}
player_info= {"name": "","position": "","team": "", "height":"", "weight":"", "picture": "", "madden_ratings": {}}
playerInfoList = []
print("program started")
playerData = {"name": '', "team": ""}
with open("playerlinks", "r") as fp:
    players = json.load(fp)

# ---------------------------------------------------------------------------------------
link0 = players[0:10]
links = players
link1 = players[0:500]
link2 = players[1001:1500]
link3 = players[1001:]
link4 = players[1001:1010]
print(len(players))
# print(link1)
# links = [players[0],players[200],players[300]]
# # ----------------------------------------------------------------------------------
# cluster = MongoClient("mongodb+srv://nicholasch24:<password>@cluster0.uuyxsu9.mongodb.net/nfl")
# collection = cluster["playerData"]
# # ----------------------------------------------------------------------------------
for link in links:
    # print(link)
    playersLinks = requests.get(link).text
    soup = BeautifulSoup(playersLinks, 'html.parser')
    name = soup.find("h1", class_="header-title pt-2 mb-0").text.lstrip()
    infoBox = soup.find("div", class_="header-subtitle")

    try:
        info = infoBox.find_all("p")
        team = info[2].text.split(" ",1)[1]

    except:
        team =""

    playerData["team"] = team
    playerData["name"] = name.lstrip()


    urlName = name.replace(" ", "-")
    nflUrl = "https://www.nfl.com/players/" + urlName
    nfl_page = requests.get(nflUrl).text
    nfl_soup = BeautifulSoup(nfl_page, 'html.parser')
    soup = BeautifulSoup(playersLinks, 'html.parser')
    try:
        nflPicture = nfl_soup.find_all("img", class_="img-responsive")
        pic2 = nflPicture[3]["src"]
        repPic = pic2.replace("/t_lazy", "_2x")
        player_info["picture"] = repPic
        if "nfl.com" not in repPic:
            player_info["picture"] = ""
    except:
        player_info["picture"] = ""
    # print(repPic)
    infoBox = soup.find("div", class_="header-subtitle")
    info = infoBox.find_all("p")

    # team = info[2].text.split(" ", 1)[1]
    # info2 = info[3].text.split()
    # birthdateList = info2[4:7]
    try:
        position = info[3].text.split()[1]

    except:
        position = ""
    player_info["position"] = position
    # print(playerData["name"])

    playerPage = soup.find("div", class_="tab-content mb-4 pb-2")
    for i in range(7):
        data = playerPage.select("ul")[i]
        for li in data.find_all("li"):
            ratings = li.text
            # try:
            #     split_ratings = ratings.split(" ", 1)
            #     player_ratings["num"] = int(split_ratings[0])
            #     player_ratings["trait"] = split_ratings[1]
            # except:
            #     split_ratings = ""
            # player_ratings["num"] = ""
            # player_ratings["trait"] = ""

            split_ratings = ratings.split(" ", 1)
            if split_ratings[0] == "--":
                player_ratings["num"] = split_ratings[0]
            else:
                player_ratings["num"] = int(split_ratings[0])
                player_ratings["trait"] = split_ratings[1]
            playerData["madden_ratings"] = player_ratings
            madden_ratings[player_ratings["trait"]] = player_ratings["num"]
            slicedDict = dict(itertools.islice(madden_ratings.items(), 0, 53))
    player_info["name"] = playerData["name"]
    player_info["team"] = playerData["team"]
    player_info["madden_ratings"] = slicedDict
    playerInfoList.append(player_info.copy())
print(playerInfoList)
with open("playerdata21.json", "a") as outfile:
        json.dump(playerInfoList, outfile, indent=4)


    # for items in player_info:
    #     playerInfoList.append(items)
    #     print(items, ':', player_info[items])




        # playerInfoList.append(people)


# print(playerInfoList)

# with open("playerdata8.json", "a") as outfile:
#     json.dump(playerInfoList, outfile, indent=2)
#     print(playerInfoList)
    # playerInfoList.append(player_info)
    # for people in player_info:
    #     playerInfoList.append(player_info)
# for x in range(len(playerInfoList)):
#     print(playerInfoList[x])
# print(playerInfoList)
# for info in playerInfoList:
#     print(info)
#     with open("playerdata4.json", "w") as outfile:
#         json.dump(playerInfoList, outfile, indent=2)
# ----------------------------------------------------------------------------------
print("upload complete")
# ----------------------------------------------------------------------------------

# playersLink = requests.get(link1).text
# soup = BeautifulSoup(playersLink, 'html.parser')
# # name = soup.find("h1", class_="header-title pt-2 mb-0").text
# infoBox = soup.find("div", class_="header-subtitle")
# info = infoBox.find_all("p")
# team = info[2].text.split(" ",1)[1]
# info2 = info[3].text.split()
# position = info[3].text.split()[1]
# birthdateList = info2[4:7]
# birthdate = " ".join(birthdateList)
# height = info2[10]
# weight = info2[14]
# madden_ratings= {}
# playerPage = soup.find("div", class_="tab-content mb-4 pb-2")
# for i in range(7):
#     data = playerPage.select("ul")[i]
#     for li in data.find_all("li"):
#         ratings = li.text
#         split_ratings = ratings.split(" ", 1)
#         player_ratings["num"] = int(split_ratings[0])
#         player_ratings["trait"] = split_ratings[1]
#         playerData["madden_ratings"] = player_ratings
        # for key, val in zip( player_ratings["trait"],player_ratings["num"]):
        #     madden_ratings[key] = val
        #     print(madden_ratings)
        # madden_ratings[player_ratings["trait"]] = player_ratings["num"]



# teamLinkPage = "https://www.maddenratings.com/teams"
# teamPage = requests.get(teamLinkPage).text
# soup = BeautifulSoup(teamPage, 'html.parser')
# teams = soup.find_all("div", class_="card-body pt-3 ml-n2 pl-0 pr-2")
# for link in teams:
#     teamLinks = link.find("a")['href']
#     teamLinkList.append(teamLinks)
# print(teamLinkList)
#
# with open("teamLinks", "w") as f:
#     for line in teamLinkList:
#         f.write("%s\n" % line)

