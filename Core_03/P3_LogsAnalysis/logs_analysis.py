#! /usr/bin/env python


# "Database code" for the Logs Analysis Project
'''
db architecture
-
authors: name | bio | id
articles: author-id | title | slug | lead | body | time | article-id
log: path | ip | method | status | time | id

Report1:
What are the most popular three articles of all time?
* Sum the views in log per path and match to article slug in articles
 group by article title
 order descending and limit to 3 results

Report2:
Who are the most popular article authors of all time?
* Sum the views in log per path and match to article slug in articles
group by author
order descending results

Report3:
On which days did more than 1% of requests lead to errors?
* Create a view to sum views in log group by date
* Create
'''

# Import libraries
import psycopg2

# Define the database name
DBNAME = "news"

# Define the queries
# Test queries
test_1 = "select author from articles"
test_2 = "select * from authors"
test_3 = "select title, name " \
         "from articles join authors " \
         "on articles.author = authors.id;"
test_4 = "select title, name " \
         "from articles, authors " \
         "where articles.author = authors.id;"
test_5 = "select * from log " \
         "limit 20;"

# Report queries
query_1 = "select articles.title, count(*) as views " \
           "from articles join log " \
           "on articles.slug = split_part(path,'/',3) " \
           "group by articles.title " \
           "order by views desc " \
           "limit 3;"

# Create report list object
report_1 = [query_1, None]

query_2 = "select authors.name, views " \
           "from authors, " \
           "(select articles.author, count(*) as views " \
           "from articles join log " \
           "on articles.slug = split_part(path,'/',3) " \
           "group by articles.author " \
           "order by views desc) " \
           "as aut " \
           "where aut.author = authors.id " \
           ";"

# Create report list object
report_2 = [query_2, None]

# Views to modularize report 3
view_3a = "Create view TotalViews as " \
          "select time ::timestamp::date as date, count(*) as tot_views " \
          "from log " \
          "group by date " \
          "order by tot_views desc; "

view_3b = "Create view ErrViews as " \
          "select time ::timestamp::date as date, count(*) as err_views " \
          "from log " \
          "where status = '404 NOT FOUND' " \
          "group by date " \
          "order by err_views desc; "

view_3c = "Create view ErrDaily as " \
          "select ErrViews.date, " \
          "cast(ErrViews.err_views as decimal) " \
          "/ cast(TotalViews.tot_views as decimal) " \
          "as err_daily " \
          "from TotalViews join ErrViews " \
          "on TotalViews.date = ErrViews.date " \
          "order by err_daily desc; "

query_3 = "select date, err_daily*100 " \
           "from ErrDaily " \
           "where round((err_daily)*100, 4) > 1.0; "

# Create report list object
report_3 = [query_3, [view_3a, view_3b, view_3c]]

# Add reports to list
analysis_reports = [report_1, report_2, report_3]


def generate_analysis(_database, _reports):
    '''
    Function to connect to database and run analysis
    :param _database: Name of the database as string
    :param _reports: PSQL formatted command(s) as list
    :return: None - prints query results
    '''

    if _database and _reports:
        for i in range(0, len(_reports)):
            try:
                # Connect to the database
                db = psycopg2.connect(database=_database)
                # Create a cursor object to parse the DB
                c = db.cursor()

                # Create any database views defined
                if _reports[i][1]:
                    # Loop through views
                    for v in _reports[i][1]:
                        c.execute(v)

                # Execute any queries defined
                if _reports[i][0]:
                    # Execute the query
                    c.execute(_reports[i][0])
                    # Store results
                    results = c.fetchall()
                    # Print results
                    print_report(results, i)
                # Close the connection to the database
                db.close()
            except BaseException:
                print("Unable to connect to database and fetch results.")
    else:
        print("generate_analysis function inputs missing")


def print_report(_results, _type):
    '''
    Function to print report based on type
    :param _results: Report results as list
    :param _type: Type of formatting for printing to termainal as integer
    :return: None - prints formatted results
    '''

    # If results are present
    if _results:
        # Print report header
        if _type == 0:
            print("* Report 1. What are the "
                  "most popular three articles of all time? *")
        elif _type == 1:
            print("* Report 2. Who are the "
                  "most popular article authors of all time? *")
        elif _type == 2:
            print("* Report 3. On which days did more than "
                  "1% of requests lead to errors? *")
        else:
            print("* No report style specified. *")

        # Loop through the results items
        for item in _results:
            # Print style 0
            if _type == 0:
                print("\"" + item[0].title() +
                      "\"" + " -- " + str(item[1]) + " views")
            elif _type == 1:
                print(item[0].title() +
                      " -- " + str(item[1])+" total views")
            elif _type == 2:
                print(item[0].strftime('%Y-%B-%d') +
                      " -- " + str(round(item[1], 4))+" %")
            else:
                print(item)

        # Print a break
        print("--")

    else:
        print("No results to print")


if __name__ == "__main__":
    results = generate_analysis(DBNAME, analysis_reports)
