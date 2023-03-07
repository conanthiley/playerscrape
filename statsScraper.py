import pandas as pd
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
import requests

cluster = MongoClient("mongodb+srv://nicholasch24:<Password>@cluster0.uuyxsu9.mongodb.net/nfl")
db = cluster["nfl"]
collection = db["players"]



# url = "https://www.nfl.com/players/kenny-pickett/stats/career"
# url = "https://www.nfl.com/players/velus-jones/stats/career"



# print(len(df))
for doc in collection.find():
    stats = []
    nfl_url = doc["nfl_link"]
    if len(nfl_url) < 6:
        query = ""
    else:
        url = nfl_url + "/stats/career"
        print(url)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        try:
            dframe = pd.read_html(url)
            for i in range(len(dframe)):
                df = pd.read_html(url)[i]
                table_title = soup.find_all("h3", class_="d3-o-section-sub-title")[i].text
                # print(table_title)

                table_json = df.to_json(orient='records')
                data = {"title": table_title, "data": json.loads(table_json)}
                d = data["data"]
                print(data)
                stats.append(data)
            # player_stats = stats.copy()
            # print(player_stats)
                query = {"full_name": doc["full_name"]}
                update = {"$set": {"stats": stats.copy()}}
                collection.update_one(query, update)
        except:
            print("missing data")

    # print(stats)




