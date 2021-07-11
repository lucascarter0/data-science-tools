# -*- coding: utf-8 -*-
"""
Web scraper to compile episode information for televsion shows from IMDB.

Input argument:
    index: URL index from IMDB episode page (see example).

DataFrame output:
    Season Number
    Episode Number
    Original Airdate
    Rating
    Total Rating Votes
    Episode Title
    Episode Description

Example:
    # Load episode info for Seinfeld (https://www.imdb.com/title/tt0098904/)
    df = get_imdb_ratings.load('tt0098904')

"""

import bs4
from bs4 import BeautifulSoup
from requests import get
import pandas as pd



def log_text(element: bs4.element.Tag):
    """ Return text of a Beautiful Soup element if the element is populated,
    else return None."""
    return element.text.strip() if element is not None else None



def format_votes(value: str):
    """ Transform votes information from IMDB to a more useable format.
    Example: format_votes("(1,789)") returns "1789". """
    if isinstance(value, str):
        value = value.replace('(', '').replace(')', '').replace(',', '')
    return value



class UrlInfo:
    """ Class to handle all url parsing operations. Parses top-level show info
    as well as each specific season. """

    baseurl = 'https://www.imdb.com/title'

    def __init__(self, url_index: str):
        self.url = '{}/{}'.format(self.baseurl, url_index)
        self.__parse_season_list()

    def __parse_season_list(self):
        url = '{}/episodes'.format(self.url)
        html_soup = self.html_soup_object(url)

        season_filter_element = html_soup.find('select', attrs={'id': 'bySeason'})
        self.number_of_seasons = len(season_filter_element.find_all('option'))
        self.title = html_soup.find('a', attrs={'class': 'subnav_heading'}).text

    def episode_list(self, season: str):
        """ Return list of BeautifulSoup objects.
        Each element in the list corresponds to a season in the show."""
        url = '{}/episodes?season={}'.format(self.url, season)
        return self.html_soup_object(url).find_all('div', class_='info')

    @staticmethod
    def html_soup_object(url: str):
        """ Parse a URL string and return the URL info as a BeautifulSoup
        object."""
        response = get(url)
        return BeautifulSoup(response.text, 'html.parser')



def load(show_index: str):
    """Web scraper to compile episode information for televsion shows from IMDB.
    Return of pandas dataframe of episode info for a television show given
    the show's url index.

    Example:
        # Load episode info for Seinfeld (https://www.imdb.com/title/tt0098904/)
        df = get_imdb_ratings.load('tt0098904')
    """


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

    numeric_columns = ['episode', 'rating', 'total_votes']
    info_df = pd.DataFrame(episode_list)
    info_df['total_votes'] = info_df['total_votes'].apply(format_votes)
    info_df[numeric_columns] = info_df[numeric_columns].apply(pd.to_numeric)
    return info_df
