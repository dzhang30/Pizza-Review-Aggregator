import requests
from bs4 import BeautifulSoup


CLIENT_ID = 'h9Hv2QQaM4-YX8MGZheEjw'
CLIENT_SECRET = 'tgxLocnJYlM2Pc9iWq2sOwzlKLXSqfZyI4alwhoBZTzwgqOG6ZQIDm8D27qptZCI'

API_HOME = 'https://api.yelp.com'
AUTH_TOKEN_PATH = '/oauth2/token'
SEARCH_PATH = '/v3/businesses/search'
GRANT_TYPE = 'client_credentials'

LOCATION = 'New York, NY'
CATEGORY = ['pizza']
LIMIT = 5


class Yelp(object):

    def __init__(self):
        self.sessions = requests.session()
        self._authenticate()
        self._set_headers()

    def _authenticate(self):
        """
        Authenticate with Yelp's API via OAuth2 and sets the Bearer Token
        """
        url = '{0}{1}'.format(API_HOME, AUTH_TOKEN_PATH)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': GRANT_TYPE}

        response = self.sessions.post(url=url, headers=headers, data=data)
        self.bearer_token = response.json()['access_token']

    def _set_headers(self):
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}
        self.sessions.headers.update(headers)

    def search_pizza_restaurant(self, restaurant_name):
        """
        Search for the input pizza restaurant via Yelp
        :param restaurant_name: (str) name of pizza restaurant
        :return: list of restaurant(s) that match the input name
        """
        url = '{0}{1}'.format(API_HOME, SEARCH_PATH)
        params = {'term': restaurant_name, 'location': LOCATION, 'categories': CATEGORY, 'limit': LIMIT}
        response = self.sessions.get(url=url, params=params)
        restaurants = response.json()['businesses']

        result = []
        for restaurant in restaurants:
            if restaurant['name'].lower() == restaurant_name.lower():
                result.append(restaurant)

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
            {'review': review.getText(), 'rating': float(rating['content ']), 'date': date['content']}
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
