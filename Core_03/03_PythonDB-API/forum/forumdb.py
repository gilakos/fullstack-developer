# "Database code" for the DB Forum.
import psycopg2
import bleach
import datetime

POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME = "forum"

def get_posts():
    """Return all posts from the 'database', most recent first."""
    # Define the database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to parse the DB
    c = db.cursor()
    # Execute a query
    c.execute("select content, time from posts order by time desc")
    # Return the results
    return c.fetchall()
    # Close the connection
    db.close()

def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    # Define the database
    db = psycopg2.connect(database=DBNAME)
    # Create a cursor object to parse the DB
    c = db.cursor()
    # Execute a query
    c.execute("insert into posts values (%s)", (bleach.clean(content),))
    # Commit the insertion
    db.commit()
    # Close the connection
    db.close()


