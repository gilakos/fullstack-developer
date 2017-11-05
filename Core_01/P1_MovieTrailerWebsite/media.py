# Import necessary libraries
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
        self.poster = _poster
        self.trailer = _trailer

    def show_trailer(self):
        '''
        Launches video window
        :return:
        '''
        webbrowser.open(self.trailer)