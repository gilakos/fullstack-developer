# Import local modules
import media
import fresh_tomatoes
# Import libraries
import webbrowser
import http.client
import requests

# Define urls for themoviedb.org api discovery
api_cred = "?api_key=0ea0de5b42e92ce5329074cc3dbff432"
# url for current released movies
discover_url = "https://api.themoviedb.org/3/discover/movie?api_key=0ea0de5b42e92ce5329074cc3dbff432&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&primary_release_year=2017"

# Query the api
response = requests.get(discover_url)
data = response.json()
movies_db = data['results']

# Define urls for additional api requests and posters/vidoes
movie_url = "https://api.themoviedb.org/3/movie/"
yt_base_url="https://www.youtube.com/watch?v="
img_base_url="https://image.tmdb.org/t/p/original/"

all_movies = []
movie_counter = 0
max_movies = 12
for m_db in movies_db:
    # Limit the number of movie objects to create
    if movie_counter >= max_movies:
        break

    # Use main response for basic movie information
    print(m_db['original_title'])
    #print(m_db['overview'])

    # Get the poster url with an additional api request
    get_poster_url = movie_url+str(m_db['id'])+"/images"+api_cred
    poster_response = requests.get(get_poster_url)
    poster_data = poster_response.json()
    poster_url = img_base_url+poster_data['posters'][0]['file_path']
    #print(poster_url)

    # Get the video url with an additional api request
    get_trailer_url = movie_url+str(m_db['id'])+"/videos"+api_cred
    trailer_response = requests.get(get_trailer_url)
    trailer_data = trailer_response.json()
    trailer_url = yt_base_url+trailer_data['results'][0]['key']
    #print(trailer_url)

    all_movies.append(media.Movie(m_db['original_title'],m_db['overview'],poster_url,trailer_url))
    movie_counter+=1

# Oen webpage
fresh_tomatoes.open_movies_page(all_movies)