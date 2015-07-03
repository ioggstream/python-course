# Fabric 

##Fabric Orchestrator
You can try everything from here

        git clone https://github.com/ioggstream/mysql-community
        cd mysql-community/fabric


## Fabric - HLA
A python framework for managing, replicating and scaling mysql servers.

  -  aggregate servers in high availability groups
  -  configure single-master replication topologies
  -  monitor and heal failures
  -  director for rw/split
  -  fabric connectors (caching db topology)

\iffalse
%http://mysqlmusings.blogspot.it/2013/10/mysql-fabric-high-availability-groups.html
\fi


## Fabric - HLA

\includegraphics[height=6.6cm,width=12cm]{images/mysql-fabric-hla.jpg}


## mysqlfabric
```mysqlfabric``` commands:

  -  manage - setup and manage fabric service
  -  group - administer high availability groups
  -  server - manage, clone, provision and decommission servers
  -  provider - manage server providers (eg. openstack, ...)

Further functionalities:

  -  statistics, dump, role, user,
  -  threat, snapshot, event


## Setup

Basic Setup is just specifying in `/etc/fabric.cfg`

  - listening ports for xmlrpc service
  - admin user (eg. $fabric$ to manage servers)
  - applicative user credentials
  
Then

    mysqlfabric manage [setup|start|ping|stop|teardown]
    mysqlfabric manage setup
    mysqlfabric manage start --daemon


## Replication Groups    

Groups are managed via

    mysqlfabric group [create|add|promote|activate] $GROUP

Crete an High Availability group and add a bunch of
servers.

    mysqlfabric group create $GROUP
    mysqlfabric group add $GROUP my-host-1:3306    
    mysqlfabric group add $GROUP my-host-2:3306

\hspace*{3cm}\includegraphics[height=4cm]{images/mysql-fabric-hagroup.png}


##Replication Groups
Promote one server as a master. 
    
    mysqlfabric group promote $GROUP

Show the server group

    mysqlfabric group lookup_servers ha
    Fabric UUID:  5ca1ab1e-a007-feed-f00d-cab3fe13249e
    Time-To-Live: 1
    server_uuid     address    status      mode weight
    ------------------------------------ ----------- --------- --------- ------
    2cda700e-1eaa-11e5-957c-0242ac110015 172.17.0.21 PRIMARY   READ_WRITE   1.0
    2cda700e-1eaa-11e5-957c-0242ac110016 172.17.0.22 SECONDARY READ_ONLY    1.0
    2cda700e-1eaa-11e5-957c-0242ac110017 172.17.0.23 SECONDARY READ_ONLY    1.0


##Replication Groups
Fabric support spare servers.
 
    mysqlfabric server set_status $UUID spare

Monitoring failover and deactivating the master. 
    
    mysqlfabric group activate $GROUP
    mysqladmin -h $MASTER shutdown
    
Checking group healt we'll see that...
    
    mysqlfabric group health ha

                                    uuid is_alive    status is_not_running is_not_configured io_not_running sql_not_running io_error sql_error
    ------------------------------------ -------- --------- -------------- ----------------- -------------- --------------- -------- ---------
    2cda700e-1eaa-11e5-957c-0242ac110015        0    FAULTY              0                 0              0               0    False     False
    2cda700e-1eaa-11e5-957c-0242ac110016        1 SECONDARY              0                 0              0               0    False     False
    2cda700e-1eaa-11e5-957c-0242ac110017        1   PRIMARY              0                 0              0               0    False     False



## Importing and checking data
Import data and check replication status using python tools.

```
mysqldbimport --server=$MASTER ... sakila.sql
mysqldbcompare --server1=$MASTER --server2=$SLAVE 
  --all
```


## Connecting programmatically
    
    from mysql.connector import connect, fabric
    # Ask for a connection to the fabric server.
    c = connect(fabric={host: .., port: .., user: ..},
        autocommit=True,
        database='sample', **sql_user)
        
    # Fabric will point you to a suitable host
    #  - in this case the master - of the given
    #  group
    c.set_property(mode=fabric.MODE_READWRITE, group="my-cluster-1")


#Provisioning
## Provisioning a new slave I
Fabric uses `mysqldump` + `mysql` internally to clone a new slave.

        # Always reset TARGET configuration 
        # before reinitializing
        mysql -e '
        SET @SESSION.SQL_LOG_BIN=0;
        STOP SLAVE;
        RESET MASTER;
        '
        
        mysqlfabric server clone $GROUP $TARGET


## Provisioning a failed master

Reingesting a failed master is not trivial.
 
  - non-replicated transactions;
  - corrupt data;
   
Always reset it!

        mysqlfabric server set_status  f484d0ed-ecea-11e4-9118-0242ac110039  spare
        mysqlfabric server set_status  f484d0ed-ecea-11e4-9118-0242ac110039  secondary


#Fabric + Docker
## Provisioning new container via docker
Show the provisioning interface (docker, openstack). 

    # mysql.fabric.providers.dockerprovider
    class MachineManager(AbstractMachineManager):
        """Manage Docker Containers."""
        def create(self, parameters, wait_spawning):
            ...
        def search(self, generic_filters, meta_filters):
            ...
        def destroy(self, machine_uuid):
            ...


## Docker Provisioning

    # Register a provider (requires docker in http)
    mysqlfabric provider register mydocker 
        user password 
        http://172.17.42.1:2375  
        --provider_type=DOCKER

    # Create or remove new servers
    mysqlfabric server create mydocker 
        --image=name=mysql-fabric   
        --flavor=name=v1            
        --meta=command="mysqld --log-bin=foo"

    # List servers
    mysqlfabric server list docker


## Wrap Up

  -  Replication is easier with Fabric and MySQL 5.6
  -  You can clone servers
  -  Failover is just one command ahead
  -  You can't re-ingest failed masters (luckily;)
  -  Try Fabric with Docker!


## That's all folks!

Thank you for the attention! 
\\insertauthor
