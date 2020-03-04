import requests
import re
import telebot
from bs4 import BeautifulSoup
from telebot import types


class YoutubeParser:
    def __init__(self):
        self.music_links = {}
        self.markups = None

    def get_music_links(self, music_name):
        music = music_name.replace(' ', '+')
        r = requests.get("https://www.youtube.com/results?search_query={}".format(music))
        soup = BeautifulSoup(r.text)
        videos = soup.findAll("div", {"class": "yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix"})
        for i in videos[:5]:
            try:
                name = i.div.h3.a.string.replace('`', '')
                href = 'https://www.youtube.com/watch?v=' + str(re.findall("\?v\=(.+?)\"|$", i.__str__())[0])
                self.music_links[name] = href
            except Exception:
                continue

    def get_music_markups(self):
        self.markups = telebot.types.InlineKeyboardMarkup()
        for href in self.music_links:
            self.markups.add(types.InlineKeyboardButton(href, callback_data='YBM{}'.format(href)))
        return self.markups

    def get_music_href(self, name):
        return self.music_links[name]


# if __name__ == '__main__':
#     Y = YoutubeParser()
#     Y.get_music_links("tamam tamam")
#     print(Y.get_music_markups())
