# summersalt_assessment
technical assessment for SummerSalt



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

