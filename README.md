# EmailTracking

#### Installation

##### Install MySQL
1. Import public key used by the package management system  
`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5`  
2. Add source to repository in the package manager  
`echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list`
3. Update local repository  
`sudo apt-get update`
4. Install mongodb packages  
`sudo apt-get install -y mongodb-org`
5. Start the mongodb server  
`sudo service mongod start`
5. Enable mongod auto restart  
`sudo systemctl enable mongod`

###### Initial Setup: Create hyrelabs_db database
```
use hyrelabs_db;
db.createUser({
    "user" : "nifty_sticks_owner",
    "pwd": "U#9^B1bFqk",
    "roles" : [{role: "dbOwner", db: "nifty_sticks"}]
});  
```
_ **Tip:** Ensure either authentication is disabled, or current user has permission to create new user_


##### Install Redis  
1. Add repository  
`sudo add-apt-repository ppa:chris-lea/redis-server`  
2. Update local package information  
`sudo apt-get update`  
3. Install latest redis server  
`sudo apt-get install redis-server`  



#### Install Oracle JDK  
1. Add repository
`sudo add-apt-repository ppa:linuxuprising/java`  
2. Update local repo  
`sudo apt-get update`  
3. Install JDK  
`sudo apt-get install oracle-java10-installer`  


##### Install Solr 7.3
1. Extract Solr 7.3  
2. `cd solr-7.3.0`  
3. `./bin/solr start -e cloud`
4. Create a 1 node cluster and cancel the script when it asks for collection name
5. Create a copy of the default ConfigSet  
`cp -r server/solr/configsets/_default/ server/solr/configsets/unbxd_config`    
5. CD into project directory `nifty-sticks`  
6. Move solr config from project to solr  
`cp deployment/solr_7.3/server/solr/configsets/unbxd_config/conf/managed-schema <path-leading-to-solr>/solr-7.3.0/server/solr/configsets/unbxd_config/conf/`  
7. CD installed solr directory
5. Upload ConfigSet to ZooKeeper  
`./bin/solr zk upconfig -n unbxd_config -d server/solr/configsets/unbxd_config/ -z localhost:9983`  
