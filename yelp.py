import requests
from bs4 import BeautifulSoup

API_HOME = 'https://api.yelp.com/v3'
SEARCH_PATH = '/businesses/search'

LOCATION = 'New York, NY'
CATEGORY = ['pizza']


class Yelp(object):

    def __init__(self, api_key, limit):
        self.api_key = api_key
        self.limit = limit  # the number/limit of results you want
        self.sessions = requests.session()
        self._set_headers()

    def _set_headers(self):
        headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        self.sessions.headers.update(headers)

    def search_pizza_restaurant(self, restaurant_name):
        """
        Search for the input pizza restaurant via Yelp
        :param restaurant_name: (str) name of pizza restaurant
        :return: list of restaurant(s) that match the input name
        """
        url = '{0}{1}'.format(API_HOME, SEARCH_PATH)
        params = {'term': restaurant_name, 'location': LOCATION, 'categories': CATEGORY, 'limit': self.limit}
        response = self.sessions.get(url=url, params=params)
        restaurants = response.json()['businesses']

        result = [restaurant for restaurant in restaurants if
                  self.clean_restaurant_name(restaurant['name']) == restaurant_name]

        return result

    def get_reviews_and_ratings(self, restaurant_url, n):
        """
        Get the n most recent reviews and corresponding scores for the restaurant
        :param restaurant_url: (str) url to restaurant on Yelp
        :param n: (int) number of most recent reviews and corresponding scores to retrieve (n < 10)
        :return: list of reviews & scores (i.e. [['...', 4], ['...', 2], ['...', 5]] )
        """
        url = '{0}&{1}'.format(restaurant_url, 'sort_by=date_desc')
        response = self.sessions.get(url=url)
        soup = BeautifulSoup(response.content, 'html.parser')
        num_yelp_reviews = int(soup.find('span', {'itemprop': 'reviewCount'}).getText())
        n = num_yelp_reviews if num_yelp_reviews < n else n

        reviews_ratings = []
        review = soup.find('p', {'itemprop': 'description'})
        rating = soup.find('div', {'itemprop': 'reviewRating'}).find('meta', {'itemprop': 'ratingValue'})
        date = soup.find('meta', {'itemprop': 'datePublished'})
        reviews_ratings.append(
            {'review': review.getText(), 'rating': float(rating['content']), 'date': date['content']}
        )

        while n > 1:
            review = review.find_next('p', {'itemprop': 'description'})
            rating = rating.find_next('meta', {'itemprop': 'ratingValue'})
            date = date.find_next('meta', {'itemprop': 'datePublished'})
            reviews_ratings.append(
                {'review': review.getText(), 'rating': float(rating['content']), 'date': date['content']}
            )
            n -= 1

        return reviews_ratings

    @staticmethod
    def clean_restaurant_name(name):
        return name.replace('’', '').replace('\'', '').lower()
