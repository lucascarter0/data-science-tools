# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:22:54 2020

@author: lucas
"""

from requests import get
from bs4 import BeautifulSoup
import pandas as pd


def html_soup_object(url):
    response = get(url)
    return BeautifulSoup(response.text, 'html.parser')


def log_text(element):
    return element.text.strip() if element is not None else None

def format_votes(value):
    if isinstance(value, str):
        value = value.replace('(', '').replace(')', '').replace(',', '')
    return value


class UrlInfo:

    baseurl = 'https://www.imdb.com/title'

    def __init__(self, show_index):
        self.url = '{}/{}'.format(self.baseurl, show_index)
        self.__parse_season_list()

    def __parse_season_list(self):
        url = '{}/episodes'.format(self.url)
        html_soup = html_soup_object(url)

        season_filter_element = html_soup.find('select', attrs={'id': 'bySeason'})
        self.number_of_seasons = len(season_filter_element.find_all('option'))
        self.title = html_soup.find('a', attrs={'class': 'subnav_heading'}).text

    def episode_list(self, season):
        url = '{}/episodes?season={}'.format(self.url, season)
        return html_soup_object(url).find_all('div', class_='info')


# Family guy (19 seasons)
# show_index = 'tt0182576'
# The blacklist (8 seasons)
# show_index = 'tt2741602'
# Criminal Minds (15 seasons)
# show_index = 'tt0452046'
# Halt and Catch Fire (4 seasons)
# show_index = 'tt2543312'
# The Simpsons
# show_index = 'tt0096697'
# Rick and Morty
# show_index = 'tt2861424'
# Seinfeld
show_index = 'tt0098904'

show = UrlInfo(show_index)

print('Compiling episode ratings for {}, {} seasons total'.format(show.title,
                                                                  show.number_of_seasons))
episode_list = []
for season in range(1, show.number_of_seasons+1):

    episode_containers = show.episode_list(season)
    print('Season {}'.format(season))
    for container in episode_containers:
        
        info = dict()

        info['season'] = season
        info['episode'] = container.meta['content']

        airdate = container.find('div', class_='airdate')
        info['airdate'] = pd.to_datetime(log_text(airdate))

        rating = container.find('span', class_='ipl-rating-star__rating')
        info['rating'] = log_text(rating)

        votes = container.find('span', class_='ipl-rating-star__total-votes')
        info['total_votes'] = log_text(votes)

        title = container.find('a', attrs={'itemprop': 'name'})
        info['title'] = log_text(title)
        
        description = container.find('div', class_='item_description')
        info['description'] = log_text(description)

        episode_list.append(info)


df = pd.DataFrame(episode_list)
df['total_votes'] = df['total_votes'].apply(format_votes)
df[['episode', 'rating', 'total_votes']] = df[['episode', 'rating', 'total_votes']].apply(pd.to_numeric)
