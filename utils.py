import sqlite3


def movie_by_title(title):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()
    sqlite_query = f'''SELECT title, country, release_year, listed_in, description
                        FROM netflix
                        WHERE title = {title}
                        ORDER BY release_year DESC
                        LIMIT 1'''
    try:
        cur.execute(sqlite_query)
    except:
        return "not found",404
    result = cur.fetchall()
    movie_info = {"title": result[0][0], "country": result[0][1], "release_year": result[0][2], "genre": result[0][3],
     "description": result[0][4]}
    con.close()
    return movie_info, 200


def movie_by_year_range(start_year, end_year):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()
    sqlite_query = f'''SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {start_year} and {end_year}
                        ORDER BY release_year DESC
                        LIMIT 100'''
    try:
        cur.execute(sqlite_query)
    except:
        return "not found",404
    result = []
    movies = cur.fetchall()
    for i in range(len(movies)):
        result.append({"title":movies[i][0], "release_year":movies[i][1]})
    con.close()
    return result, 200

def movie_by_rating(rating):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()
    if len(rating) == 1:
        sqlite_query = f'''SELECT title, rating, description
                            FROM netflix
                            WHERE rating = {rating[0]}
                            LIMIT 100'''
    elif len(rating) == 2:
        sqlite_query = f'''SELECT title, rating, description
                            FROM netflix
                            WHERE rating = {rating[0]}
                            OR rating = {rating[1]}
                            LIMIT 100'''
    try:
        cur.execute(sqlite_query)
    except:
        return "not found",404
    result = []
    movies = cur.fetchall()
    for i in range(len(movies)):
        result.append({"title":movies[i][0], "rating":movies[i][1], "description":movies[i][2]})
    con.close()
    return result, 200


def double_actors(actor_1, actor_2):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()
    sqlite_query = f'''SELECT "cast"
                            FROM netflix
                            WHERE "cast" LIKE '%{actor_1}%'
                            AND "cast" LIKE '%{actor_2}%'
                            LIMIT 100'''
    all_actors_played = []
    try:
        for row in cur.execute(sqlite_query):
            new_cast = row[0].split(', ')
            new_cast.remove(actor_1)
            new_cast.remove(actor_2)
            all_actors_played = all_actors_played + new_cast
    except:
        return "not found",404
    actors_set = set(all_actors_played)
    result = []
    for actor in actors_set:
        if all_actors_played.count(actor) > 2:
            result.append(actor)
    con.close()
    return result, 200


def movies_by_type_release_genre(type, release_year, listed_in):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()
    sqlite_query = f'''SELECT title, description
                        FROM netflix
                        WHERE "release_year" = release_year
                        AND "listed_in" = listed_in
                        AND "type" = type
                        ORDER BY release_year DESC
                        LIMIT 100'''
    try:
        cur.execute(sqlite_query)
    except:
        return "not found",404
    result = []
    movies = cur.fetchall()
    for i in range(len(movies)):
        result.append({"title":movies[i][0], "description":movies[i][1]})
    con.close()
    return result, 200