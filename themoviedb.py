"""
Module to provide www.themoviedb.org REST calls
"""

import json
from urllib import urlencode
import requests
import media


class MovieDb():
    """
    Class that wraps REST calls - for the Movie Trailer Website Generator
    """

    def __init__(self, api_key, language):
        self.api_key = api_key
        self.language = language

    def request_list_json(self, list_id):
        """
        Makes REST call to themoviedb.org, for public list - and returns json
        Params:
        list_id - themoviedb.org public list id (number)
        """
        LIST_URL = "https://api.themoviedb.org/3/list/"
        # query_string = urlencode({"api_key": self.api_key, "language": self.language}, doseq=True)
        parm_dict = {"api_key": self.api_key, "language": self.language}
        url = LIST_URL + list_id + "?" + urlencode(parm_dict, doseq=True)
        # print url

        response = requests.get(url)
        if response.status_code != 200:
            print("Response status code: " + repr(response.status_code))
            response.close()
            return None
        json_dict = json.loads(response.text)
        response.close()

        return json_dict

    def movieid_first_video_url(self, movie_id):
        """
        Makes REST call to themoviedb.org, for movie id - and returns youtube
        video url
        Params:
        movie_id - themoviedb.org movie id (number)
        """
        YOUTUBE_URL = "https://www.youtube.com/watch?v="
        VIDEOS_URL = "https://api.themoviedb.org/3/movie/%s/videos"
        url_with_movieid = VIDEOS_URL % (movie_id)
        # query_string = urlencode({"api_key": self.api_key, "language": self.language}, doseq=True)
        parm_dict = {"api_key": self.api_key, "language": self.language}
        url = url_with_movieid + "?" + urlencode(parm_dict, doseq=True)
        # print url

        response = requests.get(url)
        json_dict = json.loads(response.text)
        response.close()

        youtube_video_key = json_dict['results'][0]['key']
        return YOUTUBE_URL + youtube_video_key

    def list_to_movie_objects(self, list_id):
        """
        Makes REST call to themoviedb.org, for online list of movies
        - and returns Movie objects
        Params:
        list_id - themoviedb.org list id (number)
        """
        IMAGE_URL = "https://image.tmdb.org/t/p/w500"

        parsed_json = self.request_list_json(list_id)

        if parsed_json is None or len(parsed_json['items']) == 0:
            return None

        movies_json = parsed_json['items']

        movies_list = []
        movie_counter = 1
        for mov in movies_json:
            # print(json.dumps(mov, indent=2))
            # print('Movie %d ...' % (movie_counter))

            movie_title = mov['title']
            movie_overview = mov['overview']
            movie_image_url = IMAGE_URL + mov['poster_path']

            movie_id = str(mov['id'])
            movie_video_url = self.movieid_first_video_url(movie_id)

            # print('Movie id: ' + movie_id)
            # print('Title: ' + movie_title)
            # print('Storyline: ' + repr(movie_overview))
            # print('Image url: ' + movie_image_url)
            # print('Video url: ' + movie_video_url)
            # print('')

            movie_object = media.Movie(movie_title,
                                       movie_overview,
                                       movie_image_url,
                                       movie_video_url)
            movies_list.append(movie_object)

            movie_counter += 1

        return movies_list
