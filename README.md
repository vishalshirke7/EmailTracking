# EmailTracking

### Tech stack


#### Installation

##### Install MySQL
1. Install Mysql version >= 5.7 

###### Initial Setup: Create hyrelabs_db database
```
create database hyrelabs_db;
use hyrelabs_db;  
```

##### Create a project on google api console for getting client_id and client_secret for Oauth(Authentication) of our application in order to log in a user using gmail and subsequently making gmail API calls for sending emails etc.

##### Project dependencies 

1. Create a virtualenv (better to work in virtualenv)  
`virtualenv env`
`cd env`
2. Add source to repository in the env 
`cd Hyrelabs`
`pip install requirements.txt`
