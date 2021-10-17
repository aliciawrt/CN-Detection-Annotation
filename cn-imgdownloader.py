import mysql.connector
import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path

# TO DO: fill in according to your credentials
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="user",
    password="password"
)

# TO DO: specify what pictures you want to download
entity_label = "ANIMAL"
entity = "lion"

mycursor = mydb.cursor()
mycursor.execute("select id_coin, side from fp.dc_coin_design_mapping, fp.cnt_pipeline_ner, fp.thrakien_images where Label_Entity=\"" + entity_label + "\" and Entity = \"" + entity + "\" and id_design = DesignID and id_coin = CoinID and ObjectType=\"original\" group by id_coin, side order by id_coin;")
myresult = mycursor.fetchall()

coin_ids = []

for x in myresult:
    coin_ids.append(x)

coin_ids = coin_ids

# Image Downloader
# Adding information about user agent
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

# check if folders exist, if not create
Path("./coins").mkdir(parents=True, exist_ok=True)
Path("./coins/" + entity).mkdir(parents=True, exist_ok=True)

for coin_id in coin_ids:

    filename = str(coin_id[0]) + ".jpg"

    # get corpus nummorum url for certain coin
    url = "https://www.corpus-nummorum.eu/coins/" + str(coin_id[0]) + "#" + coin_id[1] + "erse"

    # get html of url
    soup = bs(requests.get(url).content, "html.parser")
    # get div and img containing image url in src
    if soup.find("div", {"id": "big-image-main"}):
        if coin_id[1] == "obv":
            html_div = soup.find("div", {"id": "big-image-main"})
            html_img = html_div.find("img")
            img_url = html_img.attrs.get("src")
        else: # if reverse
            html_img = soup.find("img", {"id": "coin-second-image"})
            img_url = html_img.attrs.get("src")

        print(str(coin_id[0]) + ": " + img_url)
        # download image
        try: 
            urllib.request.urlretrieve(img_url, './coins/' + entity + '/' + filename)
        except Exception:
            pass