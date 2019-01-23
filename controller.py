from flask import Flask, render_template, request
from yelp import Yelp

API_KEY = 'rn9N_mS2vZmI3WVIq8B6PQ4SM3M7Nf1y3qyu-jQqk0jUeslme9WqVr7rmu4SvU9axWRkbjctH5yQ8rEWrDgSdaluTb9t_rmH_PScfaSqDIpUO5DtIYceJWQYkLhCWXYx'

app = Flask(__name__)

restaurants = []
yelp = Yelp(api_key=API_KEY, limit=5)


@app.errorhandler(404)
def not_found(error):
    return '404'


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_restaurant():
    if request.method == 'POST':
        restaurant_name = Yelp.clean_restaurant_name(request.form['restaurant_name'])

        global restaurants
        restaurants = yelp.search_pizza_restaurant(restaurant_name)

        return render_template('index.html', restaurants=restaurants)


@app.route('/reviews_and_ratings', methods=['POST'])
def get_reviews_and_ratings():
    if request.method == 'POST':
        i = request.form['select_restaurant']
        restaurant = restaurants[int(i)]
        num_reviews = request.form['num_reviews']
        reviews_ratings = yelp.get_reviews_and_ratings(restaurant['url'], int(num_reviews))

        average_ratings = sum(review_rating['rating'] for review_rating in reviews_ratings) / len(reviews_ratings)

        return render_template('index.html', reviews_ratings=reviews_ratings, average_ratings=average_ratings)
