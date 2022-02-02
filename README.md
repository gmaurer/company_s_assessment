# Technical Assessment
technical assessment for company



Steps to run on Mac OSX
1) CD to directory
2) run command `python3 -m venv venv`
3) run command `. venv/bin/activate`
4) install requirements: `pip install -r requirements.txt`
5) install postgresql/pgadmin and create a db within pgadmin named summersalt_db
6) run state_data.sql within query tool of pgadmin
7) run command `python3 main.py ` to execute and fill db table.  


Improvements with more time: 
1) dockerize container to build sql and python container automatically, this would improve set up as it is contained.  
2) shift the datastructure to pandas or a similar data frame to to append data in one loop.
3) sort requests to improve time complexity by removing loops of data
4) db ini file to streamline standing this up locally
5) trim down functions that manipulate the returns.  This could probably be handled by 1 function by passing in args for each column name/ list position.
6) retry functionality on queries in case of failure
7) more error handling and logging 
8) swap to mysql as this data is not geospatial in nature, I defaulted to Postgresql since it is what I am the most familar with/ could be stood up quickest. 

