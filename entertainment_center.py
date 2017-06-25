import fresh_tomatoes
import media
import themoviedb as mdb

def main():
    LANGUAGE = "en-US"

    api_key = raw_input("Enter API key: ")
    list_id = raw_input("Enter www.themoviedb.org public list id: ")

    moviedb = mdb.MovieDb(api_key, LANGUAGE)
    movies = moviedb.list_to_movie_objects(list_id)

    if movies is None or len(movies) == 0:
        print("API key or public list id is incorrect")
        return

    fresh_tomatoes.open_movies_page(movies)

if __name__ == '__main__':
    main()

