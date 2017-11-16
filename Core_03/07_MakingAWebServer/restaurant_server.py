# Import libraries
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import Base, Restaurant

# Instantiate engine
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind engine to Bass class
Base.metadata.bind = engine
# Create sessionmaker object
DBSession = sessionmaker(bind = engine)
# Interface for sqlalchemy commands (staging zone)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1><a href='/restaurants/new'>Make a new restaurant</a></h1>"
                output += "<br>"
                if restaurants:
                    for r in restaurants:
                        output += "<h1>" + r.name + "</h1>"
                        output += "<p><a href = '/restaurants/%s/edit'>Edit</a></p>"%r.id
                        output += "<p><a href = '/restaurants/%s/delete'>Delete</a></p>"%r.id
                        output += "<br>"
                else:
                    output += "Unable to connect to database"
                output += "</body></html>"

                self.wfile.write(output)
                #print(output)
                return

            if self.path.endswith("/edit"):

                # get the restaurant id
                _id = self.path.split("/")[-2]
                _rest = session.query(Restaurant).filter_by(id=_id).one()
                # proceed if successful query
                if _rest:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += _rest.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % _id
                    output += "<input name='new_restaurant_name' type='text' placeholder='%s'>" % _rest.name
                    output += "<input type='submit' value='Rename'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)


            if self.path.endswith("/delete"):

                # get the restaurant id
                _id = self.path.split("/")[-2]
                _rest = session.query(Restaurant).filter_by(id=_id).one()
                # proceed if successful query
                if _rest:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += _rest.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % _id
                    output += "<input name='confirm_restaurant_delete' type='text' placeholder='Type DELETE to Confirm'>"
                    output += "<input type='submit' value='Delete'> </form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += '''<form method='POST'
                            enctype='multipart/form-data'
                            action='/restaurants/new'>
                            <input name="new_restaurant" type="text" placeholder='New Restaurant Name'>
                            <input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)

                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant_name')

                    _id = self.path.split("/")[-2]
                    _rest = session.query(Restaurant).filter_by(id=_id).one()
                    # proceed if successful query
                    if _rest:
                        _rest.name = messagecontent[0]
                        session.add(_rest)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('confirm_restaurant_delete')

                    _id = self.path.split("/")[-2]
                    _rest = session.query(Restaurant).filter_by(id=_id).one()
                    # proceed if successful query
                    if _rest:# and messagecontent[0] == 'DELETE':
                        session.delete(_rest)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')

                    session.add(Restaurant(name=messagecontent[0]))
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print("Web server running on port: %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()