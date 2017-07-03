import unittest
from yelp import Yelp


class TestYelp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.yelp = Yelp()

    def test_search_pizza_restaurant(self):
        restaurants = self.yelp.search_pizza_restaurant('pizza hut')
        self.assertTrue(len(restaurants) > 0)

    def test_get_reviews_and_ratings(self):
        # Search pizza hut near New York, NY in Yelp, then sort reviews by Newest First. This will be the result
        url = 'https://www.yelp.com/biz/pizza-hut-new-york-9?sort_by=date_desc'
        review = 'Decently good pizza at a decent price.  The cheese tasted cheap, but you get what you pay for.\n'
        rating = 3.0

        test_result = self.yelp.get_reviews_and_ratings(restaurant_url=url, n=1)

        self.assertEqual(test_result[0]['review'], review)
        self.assertEqual(test_result[0]['rating'], rating)


if __name__ == '__main__':
    unittest.main()


