import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for song in songs:
    song_name = song.select_one('td.info > a.title.ellipsis').text.strip()
    song_artist = song.select_one('td.info > a.artist.ellipsis').text.strip()
    song_ranking = song.select_one('td.number').text[0:2].strip()
    if song_name is not None:
        print(song_ranking, song_name, song_artist)
    db.songs.insert_one({'ranking': song_ranking, 'song_name': song_name, 'song_artist': song_artist})