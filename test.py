from unittest.mock import patch

from yelp import Yelp

test_api_key = 'testabc'


@patch('yelp.requests')
def test_search_pizza_restaurant(mock_requests):
    mock_json = {
        'businesses': [
            {'name': 'pizza hut', 'loc': 'nyc'},
            {'name': 'lombardi\'s pizza', 'loc': 'harlem'},
            {'name': 'domino\'s pizza', 'loc': 'nyc'},
            {'name': 'pizza hut', 'loc': 'brooklyn'}
        ]
    }
    mock_requests.session.return_value.get.return_value.json.return_value = mock_json

    yelp = Yelp(api_key=test_api_key, limit=1)
    search_result = yelp.search_pizza_restaurant('pizza hut')
    assert search_result == [{'name': 'pizza hut', 'loc': 'nyc'}, {'name': 'pizza hut', 'loc': 'brooklyn'}]


@patch('yelp.requests')
def test_get_reviews_and_ratings(mock_requests):
    with open('test_yelp_lombardis.html') as outfile:
        test_yelp_lombardi_html = outfile.read()
    mock_requests.session.return_value.get.return_value.content = test_yelp_lombardi_html

    yelp = Yelp(api_key=test_api_key, limit=1)
    result = yelp.get_reviews_and_ratings('test_url', 1)[0]

    assert 0.0 <= result['rating'] <= 5.0  # yelp reviews will always be between 0 - 5 stars
    assert len(result['date']) == 10  # the date will always be in YYYY-MM-DD format, so 10 characters
    assert len(result['review']) > 0


def test_clean_restaurant_name():
    test_name = 'This is Yelp\'s Lombardi’s Pizza'

    assert Yelp.clean_restaurant_name(test_name) == 'this is yelps lombardis pizza'
