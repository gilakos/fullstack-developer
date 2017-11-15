# Fullstack Developer Nanodegree @ Udacity
## Gil Akos

### Project 3: Logs Analysis
A simple program for analyzing database logs.

> Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.

#### Questions to Answer
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

#### Usage
Using Brackets or similar, open the index.html file to launch a browser window.
1. Install the Virtual Machine (we are using [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1))
2. Close this repository
3. Download the [Virtual Machine Configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) and add it to this repository folder
4. Download the data `newsdata.sql` and add it to this repository folder (optionally you can add .sql to your gitignore file)
5. Launch the Virtual Machine with `$ vagrant up` and `$ vagrant ssh` in the terminal
6. Browse to the directory where `logs_analysis.py` is stored
7. Run `python logs_analysis.py` in the terminal
8. The results of the analysis will be printed in the terminal window

#### Details
Reports for the `sql` database are defined in `logs_analysis.py` as `PSQL` formatted strings in the structure `[[queries],[optional: views]]`. 

Table architecture of `news` database and pseudo code of reports defined in leading comments of `logs_analysis.py`.

Sample output stored in `analysis.txt`.

#### Views 
Three views are automatically created in `logs_analysis.py` and are defined as:
```
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
```

#### Dependencies + References
1. [Psql](http://postgresguide.com/utilities/psql.html)
2. [Psycopg2](http://initd.org/psycopg/)
