# Fabric

##Fabric Orchestrator
You can try the content of those slides downloading
code and baked docker images from here:

        git clone https://github.com/ioggstream/mysql-community
        cd mysql-community/fabric
        docker-compose scale fabric=1 slave=4

Let me know after the talk!

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


## Manage
Setup and administration is done via

    mysqlfabric manage [setup|start|ping|stop|teardown]

Configure in `/etc/fabric.cfg`

  - listening ports for xmlrpc service
  - admin user (eg. $fabric$ to manage servers)
  - applicative user credentials
  - db to store fabric data

Setup and start the service

    mysqlfabric manage setup
    mysqlfabric manage start --daemon


## Replication Groups

Groups are managed via

    mysqlfabric group [create|add|promote|activate] $GROUP


Crete an High Availability group and add a bunch of
servers.

\columnsbegin
\column[t]{0.8\textwidth}

    mysqlfabric group create $GROUP
    mysqlfabric group add $GROUP my-host-1:3306
    mysqlfabric group add $GROUP my-host-2:3306
    mysqlfabric group add $GROUP my-host-3:3306

\column[t]{0.2\textwidth}
\hfill\includegraphics[width=3cm]{images/mysql-fabric-hagroup.png}

\columnsend

##Replication Groups
Promote one server as a master, eventually picking one.

    mysqlfabric group promote $GROUP [--slave_id=UUID]

Show the server group

    mysqlfabric group lookup_servers ha
    Fabric UUID:  5ca1ab1e-a007-feed-f00d-cab3fe13249e
    Time-To-Live: 1
    server_uuid     address    status      mode weight
    ------------ ----------- --------- --------- ------
    2cda..110015 172.17.0.21 PRIMARY   READ_WRITE   1.0
    2cda..110016 172.17.0.22 SECONDARY READ_ONLY    1.0
    2cda..110017 172.17.0.23 SECONDARY READ_ONLY    1.0


##Replication Groups
Fabric support spare servers.

    mysqlfabric server set_status $UUID spare

Monitoring failover and deactivating the master.

    mysqlfabric group activate $GROUP
    mysqladmin -h $MASTER shutdown

Checking group health we'll see that...

    mysqlfabric group health ha

           uuid is_alive    status ..error status..io_error sql_error
    ----------- -------- --------- --- --- --- --- -------- ---------
    2cd..110015        0    FAULTY   0   0   0   0    False     False
    2cd..110016        1 SECONDARY   0   0   0   0    False     False
    2cd..110017        1   PRIMARY   0   0   0   0    False     False


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
## Provisioning a new slave
Fabric uses `mysqldump` + `mysql` internally to clone a new slave.

        # Always reset TARGET configuration
        # before reinitializing
        mysql -e '
        SET @SESSION.SQL_LOG_BIN=0;
        STOP SLAVE;
        RESET MASTER;
        '

Cloning doesn't attach the server to a group, nor starts the replica.

        mysqlfabric server clone $GROUP $TARGET


## Reingesting a failed master

Reingesting a failed master is not trivial.

  - non-replicated transactions;
  - corrupt data;

Always reset it!

        mysqlfabric server set_status  f484...110039  spare
        mysqlfabric server set_status  f484...110039  secondary


#Fabric in the Cloud
## Fabric in the Cloud
Fabric can provision new machines via eg. Openstack API.


We implemented a DockerProvider: deploy containers, not machines.

\columnsbegin
\column[t]{.2\textwidth}

\includegraphics[width=2cm]{images/mysql-fabric-provisioning-1.png}

\column[t]{.8\textwidth}

    # mysql.fabric.providers.dockerprovider
    class MachineManager(AbstractMachineManager):
        """Manage Docker Containers."""
        def create(self, parameters, wait_spawning):
            ...
        def search(self, generic_filters, meta_filters):
            ...
        def destroy(self, machine_uuid):
            ...


\columnsend

## Docker Provisioning

    # Register a provider (requires docker in http)
    mysqlfabric provider register mydocker
        user password
        http://172.17.42.1:2375
        --provider_type=DOCKER

    # Create or remove Containers
    mysqlfabric server create mydocker
        --image=name=ioggstream/mysql-community
        --flavor=name=v1
        --meta=command="mysqld --log-bin=foo"

    # List servers
    mysqlfabric server list docker


## Next steps
Openstack interface supports machine snapshots via NovaClient.

Docker volumes doesn't support snapshots, but something is moving
(in the experimental tree).

VM Snapshot alternatives require root access to docker host
and a FLUSH TABLES on the source container:

  - rsync on volumes
  - implement snapshot via docker volume plugins


## Wrap Up

  -  Replication is easier with Fabric and MySQL 5.6
  -  You can clone servers
  -  Failover is just one command ahead
  -  Don't re-ingest failed masters (luckily;)
  -  Try Fabric with Docker!
  -  Play with docker volumes


## That's all folks!

Thank you for the attention!


\insertauthor
