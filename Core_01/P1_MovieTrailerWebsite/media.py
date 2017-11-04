import webbrowser

class Movie():
    '''
    Basic class for movies
    '''
    def __init__(self, _title, _storyline, _poster, _trailer):
        '''
        Constructor method
        :param _title: title (string)
        :param _storyline: storyline (string)
        :param _poster: poster image url
        :param _trailer: trailer video url on youtube
        '''
        self.title = _title
        self.storyline = _storyline
        self.poster_image_url = _poster
        self.trailer_youtube_url = _trailer

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)