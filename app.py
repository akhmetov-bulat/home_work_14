# import sqlite3
from flask import Flask, request, jsonify
from utils import movie_by_title, movie_by_year_range, movie_by_rating, double_actors, movies_by_type_release_genre

app = Flask(__name__)


@app.route('/movie/title/', methods=['GET'])
def search_movie_by_title():
    title = request.args.get('title')
    if title:
        result, code = movie_by_title(title)
        return jsonify(result), code
    return "error", 400


@app.route('/movie/year/', methods=['GET'])
def search_movie_by_year_range():
    try:
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))
    except:
        return "error", 400
    if start_year and end_year:
        result, code = movie_by_year_range(start_year,end_year)
        return jsonify(result), code
    return "error", 400


@app.route('/rating/children')
def children_movie_rating():
    result, code = movie_by_rating(["'G'"])
    return jsonify(result), code


@app.route('/rating/family')
def family_movie_rating():
    result, code = movie_by_rating(["'PG'", "'PG-13'"])
    return jsonify(result), code


@app.route('/rating/adult')
def adult_movie_rating():
    result, code = movie_by_rating(["'R'", "'NC-17'"])
    return jsonify(result), code


@app.route('/actors/')
def search_double_actors():
    actor_1 = request.args.get('actor_1')
    actor_2 = request.args.get('actor_2')
    if actor_1 and actor_2:
        result, code = double_actors(actor_1,actor_2)
        print('here')
        return jsonify(result), code
    return "error", 400


@app.route('/movie/search/', methods=['GET'])
def search_movies_by_type_release_genre():
    type = request.args.get('type')
    release_year = request.args.get('release_year')
    listed_in = request.args.get('listed_in')
    if type and release_year.isdigit() and listed_in:
        result, code = movies_by_type_release_genre(type, release_year, listed_in)
        return jsonify(result), code
    return "error", 400


# @app.route('/test')
# def test():
#     con = sqlite3.connect('netflix.db')
#     cur = con.cursor()
#     sqlite_query = f'''SELECT * FROM netflix LIMIT 10'''
#     cur.execute(sqlite_query)
#     print(cur.description)
#     result = cur.fetchall()
#     return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
