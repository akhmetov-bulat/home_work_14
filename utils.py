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
        return "Internal Server Error"
    movie = cur.fetchall()[0]
    if not movie:
        return []
    movie_info = {"title": movie[0], "country": movie[1], "release_year": movie[2], "genre": movie[3],
     "description": movie[4]}
    con.close()
    return movie_info


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
        return []
    result = []
    movies = cur.fetchall()
    if not movies:
        return []
    for title, release_year in movies:
        result.append({"title":title, "release_year":release_year})
    con.close()
    return result

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
        return []
    result = []
    movies = cur.fetchall()
    if not movies:
        return result
    for title, rating, description in movies:
        result.append({"title":title, "rating":rating, "description":description})
    con.close()
    return result


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
        cur.execute(sqlite_query)
    except:
        return []
    actors = cur.fetchall()
    if not actors:
        return []
    for row in actors:
            new_cast = row[0].split(', ')
            new_cast.remove(actor_1)
            new_cast.remove(actor_2)
            all_actors_played = all_actors_played + new_cast
    actors_set = set(all_actors_played)
    result = []
    for actor in actors_set:
        if all_actors_played.count(actor) > 2:
            result.append(actor)
    con.close()
    return result


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
        return []
    movies = cur.fetchall()
    if not movies:
        return []
    result = []
    for title, description in movies:
        result.append({"title":title, "description":description})
    con.close()
    return result